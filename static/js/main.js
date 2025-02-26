/**
 * Grok OpenAI API 服务 - 主JavaScript文件
 */

document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 代码示例复制功能
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        // 创建复制按钮
        const copyButton = document.createElement('button');
        copyButton.className = 'btn btn-sm btn-primary copy-button';
        copyButton.textContent = '复制';
        copyButton.setAttribute('data-bs-toggle', 'tooltip');
        copyButton.setAttribute('data-bs-placement', 'top');
        copyButton.setAttribute('title', '复制到剪贴板');
        
        // 将按钮添加到代码块的父元素
        const pre = block.parentNode;
        pre.style.position = 'relative';
        copyButton.style.position = 'absolute';
        copyButton.style.top = '5px';
        copyButton.style.right = '5px';
        pre.appendChild(copyButton);
        
        // 添加点击事件
        copyButton.addEventListener('click', () => {
            const code = block.textContent;
            navigator.clipboard.writeText(code).then(() => {
                copyButton.textContent = '已复制!';
                setTimeout(() => {
                    copyButton.textContent = '复制';
                }, 2000);
            }).catch(err => {
                console.error('复制失败:', err);
                copyButton.textContent = '复制失败';
                setTimeout(() => {
                    copyButton.textContent = '复制';
                }, 2000);
            });
        });
    });

    // 添加API状态检查
    const apiStatusElement = document.getElementById('api-status');
    if (apiStatusElement) {
        checkApiStatus(apiStatusElement);
    }
});

/**
 * 检查API状态
 * @param {HTMLElement} statusElement - 显示状态的HTML元素
 */
function checkApiStatus(statusElement) {
    fetch('/')
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('API服务不可用');
        })
        .then(data => {
            statusElement.textContent = '在线';
            statusElement.className = 'badge bg-success';
            
            // 如果有版本信息，显示它
            const versionElement = document.getElementById('api-version');
            if (versionElement && data.version) {
                versionElement.textContent = data.version;
            }
        })
        .catch(error => {
            console.error('API状态检查失败:', error);
            statusElement.textContent = '离线';
            statusElement.className = 'badge bg-danger';
        });
}

/**
 * 发送测试请求到API
 */
function sendTestRequest() {
    const testResultElement = document.getElementById('test-result');
    const testButton = document.getElementById('test-button');
    
    if (testButton) {
        testButton.disabled = true;
        testButton.textContent = '请求中...';
    }
    
    if (testResultElement) {
        testResultElement.style.display = 'block';
        testResultElement.textContent = '发送请求中...';
        testResultElement.className = 'alert alert-info mt-2';
    }
    
    fetch('/v1/models')
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error(`API请求失败: ${response.status}`);
        })
        .then(data => {
            if (testResultElement) {
                testResultElement.textContent = '成功! API正常工作。';
                testResultElement.className = 'alert alert-success mt-2';
                
                // 显示返回的模型
                const modelsElement = document.createElement('div');
                modelsElement.className = 'mt-2';
                modelsElement.innerHTML = '<strong>可用模型:</strong> ' + 
                    data.data.map(model => model.id).join(', ');
                testResultElement.appendChild(modelsElement);
            }
        })
        .catch(error => {
            console.error('测试请求失败:', error);
            if (testResultElement) {
                testResultElement.textContent = `错误: ${error.message}`;
                testResultElement.className = 'alert alert-danger mt-2';
            }
        })
        .finally(() => {
            if (testButton) {
                testButton.disabled = false;
                testButton.textContent = '测试API';
            }
        });
} 