// Netlify Function for API
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

exports.handler = async function(event, context) {
  // 获取请求路径和方法
  const requestPath = event.path.replace('/.netlify/functions/api', '') || '/';
  const method = event.httpMethod;
  
  console.log(`处理请求: ${method} ${requestPath}`);
  console.log(`当前目录: ${process.cwd()}`);
  console.log(`__dirname: ${__dirname}`);
  
  // 列出当前目录内容
  try {
    const files = fs.readdirSync(__dirname);
    console.log(`目录内容: ${files.join(', ')}`);
  } catch (error) {
    console.error(`读取目录错误: ${error.message}`);
  }
  
  // 列出上级目录内容
  try {
    const parentDir = path.join(__dirname, '..');
    const parentFiles = fs.readdirSync(parentDir);
    console.log(`上级目录内容: ${parentFiles.join(', ')}`);
  } catch (error) {
    console.error(`读取上级目录错误: ${error.message}`);
  }
  
  // 尝试不同的脚本路径
  const possibleScriptPaths = [
    path.join(__dirname, '../../src/serverless.py'),
    path.join(__dirname, '../src/serverless.py'),
    path.join(__dirname, 'lib/src/serverless.py'),
    path.join(__dirname, 'src/serverless.py'),
    path.join(__dirname, 'serverless.py'),
    path.join(__dirname, '../serverless.py'),
    path.join(__dirname, 'lib/serverless.py'),
    path.join(__dirname, '../lib/serverless.py')
  ];
  
  let scriptPath = null;
  
  // 检查哪个路径存在
  for (const p of possibleScriptPaths) {
    console.log(`检查路径: ${p}`);
    try {
      if (fs.existsSync(p)) {
        scriptPath = p;
        console.log(`找到脚本: ${scriptPath}`);
        
        // 检查文件权限
        try {
          const stats = fs.statSync(p);
          console.log(`文件权限: ${stats.mode.toString(8)}`);
          
          // 尝试读取文件内容的前几行
          const content = fs.readFileSync(p, 'utf8').split('\n').slice(0, 5).join('\n');
          console.log(`文件内容前几行: ${content}`);
        } catch (error) {
          console.error(`读取文件信息错误: ${error.message}`);
        }
        
        break;
      }
    } catch (error) {
      console.error(`检查路径错误 ${p}: ${error.message}`);
    }
  }
  
  if (!scriptPath) {
    console.error('找不到脚本文件');
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        error: 'Server Configuration Error', 
        details: 'Script not found',
        checkedPaths: possibleScriptPaths,
        currentDir: process.cwd(),
        dirname: __dirname
      }),
      headers: { 'Content-Type': 'application/json' }
    };
  }
  
  // 检查 Python 是否可用
  try {
    const pythonVersionProcess = spawn('python', ['--version']);
    let pythonVersionOutput = '';
    let pythonVersionError = '';
    
    pythonVersionProcess.stdout.on('data', (data) => {
      pythonVersionOutput += data.toString();
    });
    
    pythonVersionProcess.stderr.on('data', (data) => {
      pythonVersionError += data.toString();
    });
    
    await new Promise((resolve) => {
      pythonVersionProcess.on('close', resolve);
    });
    
    console.log(`Python 版本: ${pythonVersionOutput.trim() || pythonVersionError.trim()}`);
  } catch (error) {
    console.error(`Python 检查错误: ${error.message}`);
  }
  
  // 添加库路径
  const libPath = path.join(__dirname, 'lib');
  process.env.PYTHONPATH = libPath;
  console.log(`PYTHONPATH: ${process.env.PYTHONPATH}`);
  
  // 检查库目录
  try {
    if (fs.existsSync(libPath)) {
      const libFiles = fs.readdirSync(libPath);
      console.log(`库目录内容: ${libFiles.join(', ')}`);
      
      // 检查 src 目录
      const srcPath = path.join(libPath, 'src');
      if (fs.existsSync(srcPath)) {
        const srcFiles = fs.readdirSync(srcPath);
        console.log(`src 目录内容: ${srcFiles.join(', ')}`);
      } else {
        console.error(`src 目录不存在: ${srcPath}`);
      }
    } else {
      console.error(`库目录不存在: ${libPath}`);
    }
  } catch (error) {
    console.error(`读取库目录错误: ${error.message}`);
  }
  
  // 构建命令参数
  const pythonPath = process.env.PYTHON_PATH || 'python';
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
      const chunk = data.toString();
      responseData += chunk;
      console.log(`Python输出: ${chunk}`);
    });
    
    pythonProcess.stderr.on('data', (data) => {
      const chunk = data.toString();
      errorData += chunk;
      console.error(`Python错误: ${chunk}`);
    });
    
    // 等待Python进程完成
    const exitCode = await new Promise((resolve) => {
      pythonProcess.on('close', resolve);
    });
    
    console.log(`Python进程退出代码: ${exitCode}`);
    
    if (exitCode !== 0) {
      console.error(`Python进程退出代码: ${exitCode}`);
      console.error(`错误: ${errorData}`);
      return {
        statusCode: 500,
        body: JSON.stringify({ 
          error: 'Internal Server Error', 
          details: errorData,
          exitCode: exitCode,
          scriptPath: scriptPath
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
        details: error.message,
        scriptPath: scriptPath
      }),
      headers: { 'Content-Type': 'application/json' }
    };
  }
}; 