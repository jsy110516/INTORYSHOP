// 모든 버튼 선택
const buttons = document.querySelectorAll('.button');

// 숫자 출력 창 선택
const display = document.querySelector('.display');

let currentNum = '0'; // 현재 입력값
let operator = null; // 연산자
let firstOperand = null; // 첫번째 피연산자

// 버튼 클릭 시 해당 버튼 값 처리
buttons.forEach(button => {
    button.addEventListener('click', () => {
        const buttonText = button.textContent;

        console.log(buttonText);

        // 숫자 버튼 클릭 시
        if (button.classList.contains('number')) {
            if (currentNum === '0') {
                currentNum = buttonText; // '0'일 경우 숫자 입력
            } else {
                currentNum += buttonText; // 숫자 이어 붙이기
            }
            display.textContent = currentNum;

        // 연산자 버튼 클릭 시
        } else if (button.classList.contains('operator')) {
            if (firstOperand === null) {
                firstOperand = currentNum; // 첫번째 피연산자 저장
            } else {
                firstOperand = calculate(firstOperand, currentNum, operator); // 이전 계산 후 첫번째 피연산자 갱신
                display.textContent = firstOperand;
            }
            operator = buttonText; // 연산자 저장
            currentNum = '0'; // 현재 입력값 초기화

            console.log(`firstOperand : ${firstOperand}, operator : ${operator}`)

        // 등호 버튼 클릭 시 계산
        } else if (buttonText === '=') {
            if (firstOperand !== null && operator !== null) {
                currentNum = calculate(firstOperand, currentNum, operator);
                display.textContent = currentNum;
                firstOperand = null;
                operator = null;
            }

        // 소수점 버튼 클릭 시
        } else if (buttonText === '.') {
            if (!currentNum.includes('.')) {
                currentNum += '.';
                display.textContent = currentNum;
            }

        // ± 버튼 클릭 시
        } else if (buttonText === '±') {
            currentNum = (parseFloat(currentNum) * -1).toString();
            display.textContent = currentNum;

        // % 버튼 클릭 시
        } else if (buttonText === '%') {
            currentNum = (parseFloat(currentNum) / 100).toString();
            display.textContent = currentNum;

        // 초기화 버튼 (C) 클릭 시
        } else if (buttonText === 'C') {
            currentNum = '0';
            operator = null;
            firstOperand = null;
            display.textContent = currentNum;
        }
    });
});

// 연산 함수
function calculate(firstOperand, secondOperand, operator) {
    firstOperand = parseFloat(firstOperand);
    secondOperand = parseFloat(secondOperand);

    switch (operator) {
        case '+':
            return (firstOperand + secondOperand).toString();
        case '-':
            return (firstOperand - secondOperand).toString();
        case '*':
            return (firstOperand * secondOperand).toString();
        case '/': // secondOperand가 0이 아닐 때 나누기 진행 0일 때는 Error 출력
            return secondOperand !== 0 ? (firstOperand / secondOperand).toString() : 'Error';
        default:
            return firstOperand.toString();
    }
}
