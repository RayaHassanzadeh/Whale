// 自动隐藏 Flash 消息
setTimeout(() => {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach((message) => {
        message.classList.remove('show');  // 移除 Bootstrap 的 "show" 类
        message.classList.add('fade');    // 添加 Bootstrap 的 "fade" 类
        setTimeout(() => message.remove(), 500);  // 确保动画完成后移除消息
    });
}, 3000); // 设置 3 秒后自动隐藏
