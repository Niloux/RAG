// 全局变量
const API_BASE_URL = 'http://localhost:8000';

// DOM 元素
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadStatus = document.getElementById('uploadStatus');
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');

// 拖放功能
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#4a90e2';
    dropZone.style.backgroundColor = '#f5f5f5';
});

dropZone.addEventListener('dragleave', () => {
    dropZone.style.borderColor = '#ddd';
    dropZone.style.backgroundColor = 'white';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#ddd';
    dropZone.style.backgroundColor = 'white';
    
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
        handleFileUpload(file);
    } else {
        showStatus('请上传PDF文件', 'error');
    }
});

// 文件选择处理
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileUpload(file);
    }
});

// 文件上传处理
async function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        showStatus('正在上传文件...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        if (response.ok) {
            showStatus(`文件上传成功：${file.name}`, 'success');
            addMessage('系统', '论文已成功上传，现在您可以开始提问了。', 'assistant');
        } else {
            showStatus(`上传失败：${data.detail}`, 'error');
        }
    } catch (error) {
        showStatus(`上传出错：${error.message}`, 'error');
    }
}

// 发送问题
async function sendQuestion() {
    const question = userInput.value.trim();
    if (!question) return;

    // 添加用户消息
    addMessage('您', question, 'user');
    userInput.value = '';

    try {
        const response = await fetch(`${API_BASE_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                top_k: 3
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            addMessage('系统', data.data.answer, 'assistant');
        } else {
            addMessage('系统', `抱歉，处理问题时出错：${data.detail}`, 'assistant');
        }
    } catch (error) {
        addMessage('系统', `网络错误：${error.message}`, 'assistant');
    }
}

// 添加消息到聊天界面
function addMessage(sender, content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = `<strong>${sender}：</strong>${content}`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 显示状态信息
function showStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = `status ${type}`;
}

// 回车发送消息
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendQuestion();
    }
}); 