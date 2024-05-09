const { Builder, By, until } = require("selenium-webdriver");

async function HeaderTests() {
  let driver = await new Builder().forBrowser("chrome").build();

  try {
    // Navigate to Login page
    await driver.get("http://localhost:3000/peoples_budget/login");
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Navigate to Home page
    await driver.findElement(By.id("loginGuest")).click();

    await new Promise((resolve) => setTimeout(resolve, 4000));

    // Click on header image
    await driver.findElement(By.css('img[alt="profilePhoto"]')).click();

    // Wait for popup to appear
    await driver.wait(until.elementLocated(By.id("popWindow")), 2000);
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Click on logout button
    await driver.findElement(By.id("logout")).click();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Wait for page to load
    await driver.wait(
      until.urlIs("http://localhost:3000/peoples_budget/login"),
      10000
    );

    // Verify navigation to Login page
    let title = await driver.getTitle();
    if (title !== "Login") {
      console.log("------------ Header test failed ------------");
    } else {
      console.log("------------ Header test passed ------------");
    }
  } finally {
    await driver.quit();
  }
};

module.exports = HeaderTests ;
