const puppeteer = require('puppeteer');

async function createPDF(url, outputFilename) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url, {waitUntil: 'networkidle0'});
    await page.pdf({ path: './pdf/' + outputFilename, format: 'A4' });
    await browser.close();
}

const url = process.argv[2]; 
const outputFilename = process.argv[3]; 

createPDF(url, outputFilename);
