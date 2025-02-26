// Netlify Function for API
const { spawn } = require('child_process');
const path = require('path');

exports.handler = async function(event, context) {
  // 获取请求路径和方法
  const requestPath = event.path.replace('/.netlify/functions/api', '') || '/';
  const method = event.httpMethod;
  
  console.log(`处理请求: ${method} ${requestPath}`);
  
  // 构建Python命令
  const pythonPath = process.env.PYTHON_PATH || 'python';
  const scriptPath = path.join(__dirname, '../../src/serverless.py');
  
  // 确保脚本路径存在
  const fs = require('fs');
  if (!fs.existsSync(scriptPath)) {
    console.error(`脚本不存在: ${scriptPath}`);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Server Configuration Error', details: 'Script not found' })
    };
  }
  
  // 添加库路径
  process.env.PYTHONPATH = path.join(__dirname, 'lib');
  
  // 构建命令参数
  const args = [
    scriptPath,
    method,
    requestPath,
    event.body || '',
    JSON.stringify(event.headers || {})
  ];
  
  console.log(`执行命令: ${pythonPath} ${args.join(' ')}`);
  
  // 收集Python进程的输出
  let responseData = '';
  let errorData = '';
  
  try {
    // 启动Python进程
    const pythonProcess = spawn(pythonPath, args);
    
    pythonProcess.stdout.on('data', (data) => {
      responseData += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      errorData += data.toString();
      console.error(`Python错误: ${data.toString()}`);
    });
    
    // 等待Python进程完成
    const exitCode = await new Promise((resolve) => {
      pythonProcess.on('close', resolve);
    });
    
    if (exitCode !== 0) {
      console.error(`Python进程退出代码: ${exitCode}`);
      console.error(`错误: ${errorData}`);
      return {
        statusCode: 500,
        body: JSON.stringify({ 
          error: 'Internal Server Error', 
          details: errorData,
          exitCode: exitCode
        }),
        headers: { 'Content-Type': 'application/json' }
      };
    }
    
    try {
      // 解析Python返回的JSON响应
      const response = JSON.parse(responseData);
      
      return {
        statusCode: response.statusCode || 200,
        body: response.body,
        headers: response.headers || {
          'Content-Type': 'application/json'
        }
      };
    } catch (error) {
      console.error('解析Python响应错误:', error);
      console.error('原始响应:', responseData);
      return {
        statusCode: 500,
        body: JSON.stringify({ 
          error: 'Error parsing response', 
          details: error.message,
          rawResponse: responseData.substring(0, 200) + (responseData.length > 200 ? '...' : '')
        }),
        headers: { 'Content-Type': 'application/json' }
      };
    }
  } catch (error) {
    console.error('执行Python脚本错误:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        error: 'Error executing Python script', 
        details: error.message 
      }),
      headers: { 'Content-Type': 'application/json' }
    };
  }
}; 