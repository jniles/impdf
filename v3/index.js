const puppeteer = require('puppeteer');

const verbose = true;

const SITE = "https://www.internationalministries.org"
const SLUG = "haiti-pigs-for-kids"
const OUTPUT = `./output/${SLUG}.pdf`

const PRINT_OPTIONS = {
  format : 'Letter',
};

const date = () => new Date().toISOString().replace('T', ' ').replace('Z', '');
const log = (text) => { if (verbose) { console.log(`[${date()}] ${text}`); } };

(async () => {
  log('starting headless Chrome.');

  try {
    const browser = await puppeteer.launch({ headless : true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
    const page = await browser.newPage();

    log('browser launched.');
    log(`navigating to ${SITE}/${SLUG}`);

    await page.goto(`${SITE}/${SLUG}`, { waitUntil: 'networkidle2' });

    log('injecting custom styles.');
    // inject custom stylesheet
    await page.addStyleTag({ path : './stylesheet.css' });

    log('rendering PDF');

    // create PDF and write out
    const options = Object.assign({}, { path : OUTPUT }, PRINT_OPTIONS);
    await page.pdf(options);

    log(`output saved to ${OUTPUT}`);

    await browser.close();
  } catch (e) {
    log(`Error: ${e.toString()}`);
  }
})();
