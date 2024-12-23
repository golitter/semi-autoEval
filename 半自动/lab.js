async function evaluateTeacher() {
    console.log("正在加载页面...");

    try {
        // 等待页面加载完毕，直到所有客观题出现
        await waitForElements('.qBox.objective.required');

        // 获取所有客观题元素
        const objectiveQuestions = document.querySelectorAll('.qBox.objective.required');
        console.log(`共找到 ${objectiveQuestions.length} 个问题。`);

        // 遍历每个客观题
        for (let idx = 0; idx < objectiveQuestions.length; idx++) {
            console.log(`正在处理第 ${idx + 1} 个问题...`);
            const question = objectiveQuestions[idx];

            // 获取选项列表
            const options = question.querySelectorAll('.option-item');

            // 获取最后一个选项（最高分）
            const highestOption = options[options.length - 1].querySelector('input');
            highestOption.click();  // 选择最高分

            console.log(`第 ${idx + 1} 个问题已选择最高分：${parseInt(highestOption.value) + 1}`);
        }

        // 等待主观题加载
        await waitForElements('.qBox.subjective.required');

        // 获取所有主观问题元素
        const subjectiveQuestions = document.querySelectorAll('.qBox.subjective.required');
        console.log(`共找到 ${subjectiveQuestions.length} 个主观问题。`);

        // 遍历每个主观问题
        for (let idx = 0; idx < subjectiveQuestions.length; idx++) {
            console.log(`正在处理第 ${idx + 1} 个主观问题...`);
            const question = subjectiveQuestions[idx];

            // 查找问题的文本框（textarea）
            const textarea = question.querySelector('.answer-textarea');
            if (textarea) {
                // 在文本框中输入答案
                const answer = "授课很好";
                textarea.value = answer;  // 设置答案
                console.log(`第 ${idx + 1} 个主观问题已回答。`);
            } else {
                console.log(`第 ${idx + 1} 个问题没有找到文本框。`);
            }
        }


        // 等待提交按钮可用
        await waitForElement('#sub');

        // 定位提交按钮
        const submitButton = document.querySelector('#sub');
        submitButton.click();  // 点击提交按钮
        console.log("点击提交按钮，等待提交...");

        // 等待警告框弹出
        await waitForAlert();

        // 处理警告框
        const alert = window.alert; // 获取警告框对象
        alert();  // 点击确认

        // 等待页面 URL 变化，确保提交成功
        await waitForUrlChange();
        console.log("评教已完成并提交。");

    } catch (error) {
        console.log("评教操作失败:", error);
    }
}

// 等待页面元素加载
function waitForElements(selector) {
    return new Promise((resolve, reject) => {
        const interval = setInterval(() => {
            if (document.querySelectorAll(selector).length > 0) {
                clearInterval(interval);
                resolve();
            }
        }, 1000);
    });
}

// 等待单个页面元素加载
function waitForElement(selector) {
    return new Promise((resolve, reject) => {
        const interval = setInterval(() => {
            if (document.querySelector(selector)) {
                clearInterval(interval);
                resolve();
            }
        }, 1000);
    });
}

// 等待页面 URL 发生变化
function waitForUrlChange() {
    return new Promise((resolve) => {
        const initialUrl = window.location.href;
        const interval = setInterval(() => {
            if (window.location.href !== initialUrl) {
                clearInterval(interval);
                resolve();
            }
        }, 1000);
    });
}

// 等待警告框弹出
function waitForAlert() {
    return new Promise((resolve) => {
        const interval = setInterval(() => {
            if (window.alert) {
                clearInterval(interval);
                resolve();
            }
        }, 1000);
    });
}

// 执行评教操作
evaluateTeacher();
