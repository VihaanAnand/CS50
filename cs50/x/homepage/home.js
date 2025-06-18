let bio = document.querySelector("#bio");
let greetings = ["How's your day going?", "What's up?", "How's life?", "Pleased to meet you.", "What's cooking?"];
let randomGN = Math.floor(Math.random() * greetings.length);
let greeting = greetings[randomGN];

let date = new Date();
let schoolstatus = "";
let year = date.getFullYear();
let month = date.getMonth() + 1;
let grade = year - 2017;
if (grade <= 12 && grade >= 1) {
        if (month == 6 || month == 7) {
                schoolstatus += `I'm about to go to ${grade}${grade == 1 ? "st" : (grade == 2 ? "nd" : (grade == 3 ? "rd" : "th"))} grade.`;
        }
        else if (month < 6) {
                        schoolstatus += `I'm in ${grade - 1}${grade - 1 == 1 ? "st" : (grade - 1 == 2 ? "nd" : (grade - 1 == 3 ? "rd" : "th"))} grade.`;
        }
        else {
                        schoolstatus += `I'm in ${grade}${grade == 1 ? "st" : (grade == 2 ? "nd" : (grade == 3 ? "rd" : "th"))} grade.`;
        }
}

bio.innerHTML = `Hi! I'm Vihaan Anand. ${greeting} ${schoolstatus} My favourite subject is computer science. Whenever I can, I am (almost) always coding something. Take a look at some of my projects in the "What I've been doing" tab. Another thing I love is maths. So far, I have skipped two grades in math. At home, I am studying trigonometry.`