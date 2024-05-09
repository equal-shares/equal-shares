const { Builder, By } = require("selenium-webdriver");

async function ResultsTests() {
  let driver = await new Builder().forBrowser("chrome").build();

  try {
    // Navigate to Login page
    await driver.get("http://localhost:3000/peoples_budget/login");
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Navigate to Home page
    await driver.findElement(By.id("loginGuest")).click();

    await new Promise((resolve) => setTimeout(resolve, 3200));

    // Navigate to Results page
    await driver.findElement(By.linkText("Results")).click();
    await new Promise((resolve) => setTimeout(resolve, 5000));

    // Click on Algo 1 button
    await driver.findElement(By.id("algo1")).click();
    await new Promise((resolve) => setTimeout(resolve, 3500));

    // Verify graph 1 is displayed
    let graph1 = await driver.findElement(By.id("algo1"));

    await driver.findElement(By.id("בטחון וסדר ציבורי")).click();
    await new Promise((resolve) => setTimeout(resolve, 1500));
    await driver.findElement(By.id("בטחון")).click();
    await new Promise((resolve) => setTimeout(resolve, 1500));
    await driver.findElement(By.id("בטחון וסדר ציבורי")).click();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    if (graph1.isDisplayed()) {
      console.log("------------ Results: Algo1 test passed ------------");
    } else {
      console.log("------------ Results: Algo1 test failed ------------");
    }

    // // Wait for graph to load
    // await new Promise((resolve) => setTimeout(resolve, 4000));

    // Click on Algo 2 button
    await driver.findElement(By.id("algo2")).click();
    await new Promise((resolve) => setTimeout(resolve, 3500));

    // Verify graph 2 is displayed
    let graph2 = await driver.findElement(By.id("algo2"));

    await driver.findElement(By.id("בטחון וסדר ציבורי")).click();
    await new Promise((resolve) => setTimeout(resolve, 1500));
    await driver.findElement(By.id("בטחון")).click();
    await new Promise((resolve) => setTimeout(resolve, 1500));
    await driver.findElement(By.id("בטחון וסדר ציבורי")).click();
    await new Promise((resolve) => setTimeout(resolve, 100));

    if (graph2.isDisplayed()) {
      console.log("------------ Results: Algo2 test passed ------------");
    } else {
      console.log("------------ Results: Algo2 test failed ------------");
    }

    // Wait for graph to load
    await new Promise((resolve) => setTimeout(resolve, 2500));
  } finally {
    await driver.quit();
  }
};

module.exports = ResultsTests;
