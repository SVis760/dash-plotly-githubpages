const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Replace with your local app URL
  await page.goto('http://127.0.0.1:8050/dash-plotly-githubpages/', { waitUntil: 'networkidle0' });

  // Optionally, wait for a specific element that confirms data is rendered.
  await page.waitForSelector('#data-table');

  // Get the full page content after rendering.
  const html = await page.content();

  // Save the HTML snapshot.
  fs.writeFileSync('static_index.html', html);

  await browser.close();
  console.log('Snapshot saved as static_index.html');
})();
