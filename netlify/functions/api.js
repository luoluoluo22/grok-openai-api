// Netlify Function for API
const { spawn } = require('child_process');
const path = require('path');

exports.handler = async function(event, context) {
  // 获取请求路径和方法
  const path = event.path.replace('/.netlify/functions/api', '');
  const method = event.httpMethod;
  
  // 构建Python命令
  const pythonProcess = spawn('python', [
    path.join(__dirname, '../../src/serverless.py'),
    method,
    path,
    event.body || '',
    JSON.stringify(event.headers)
  ]);
  
  // 收集Python进程的输出
  let responseData = '';
  let errorData = '';
  
  pythonProcess.stdout.on('data', (data) => {
    responseData += data.toString();
  });
  
  pythonProcess.stderr.on('data', (data) => {
    errorData += data.toString();
  });
  
  // 等待Python进程完成
  return new Promise((resolve, reject) => {
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error(`Python process exited with code ${code}`);
        console.error(`Error: ${errorData}`);
        resolve({
          statusCode: 500,
          body: JSON.stringify({ error: 'Internal Server Error', details: errorData })
        });
        return;
      }
      
      try {
        // 解析Python返回的JSON响应
        const response = JSON.parse(responseData);
        
        resolve({
          statusCode: response.statusCode || 200,
          body: response.body,
          headers: response.headers || {
            'Content-Type': 'application/json'
          }
        });
      } catch (error) {
        console.error('Error parsing Python response:', error);
        resolve({
          statusCode: 500,
          body: JSON.stringify({ error: 'Error parsing response', details: error.message })
        });
      }
    });
  });
}; 