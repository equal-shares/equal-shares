const { Builder, By, until } = require("selenium-webdriver");

async function InfoPageTests() {
  let driver = await new Builder().forBrowser("chrome").build();

  try {
    // Navigate to Login page
    await driver.get("http://localhost:3000/peoples_budget/login");
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Navigate to Home page
    await driver.findElement(By.id("loginGuest")).click();

    await new Promise((resolve) => setTimeout(resolve, 3200));

    // Navigate to Information page
    await driver.findElement(By.linkText("Information")).click();
    await new Promise((resolve) => setTimeout(resolve, 2500));

    // Wait for page to load
    await driver.wait(
      until.urlIs("http://localhost:3000/peoples_budget/information"),
      10000
    );

    // Open the first card
    await driver.findElement(By.id("0")).click();
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Click on the close button to close the card
    await driver.findElement(By.id("close-button0")).click();
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Open the second card
    await driver.findElement(By.id("4")).click();
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Click on the close button to close the card
    await driver.findElement(By.id("close-button4")).click();
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Open the third card
    await driver.findElement(By.id("7")).click();
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Click on the close button to close the card
    await driver.findElement(By.id("close-button7")).click();
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Verify navigation to Information page
    const title = await driver.getTitle();
    if (title !== "Information") {
      console.log("------------ Information tests failed ------------");
    } else {
      console.log("------------ Information tests passed ------------");
    }

    // Perform additional tests or assertions on the Information page as needed
  } finally {
    await driver.quit();
  }
};

module.exports = InfoPageTests;
