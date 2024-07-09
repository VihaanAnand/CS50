function sendEmail() {
        let email = document.querySelector("#email").value;
        let phonenumber = document.querySelector("#phonenumber").value;
        let name = document.querySelector("#name").value;
        let subject = document.querySelector("#subject").value;
        let cc = document.querySelector("#cc").value;
        let bcc = document.querySelector("#bcc").value;
        let body = document.querySelector("#body").value;
        let uri = `mailto:vihaan.s.anand@gmail.com?subject=${encodeURI(subject)}&cc=${encodeURI(cc)}&bcc=${encodeURI(bcc)}&body=${encodeURI(`${body}\n\nPlease reach me at:\nEmail: ${email}\nPhone Number: ${phonenumber}\nName: ${name}`)}`;
        window.open(uri);
}