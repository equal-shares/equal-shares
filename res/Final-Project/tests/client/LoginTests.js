const { Builder, By, Key, until } = require("selenium-webdriver");

async function LoginTests() {
  let driver = await new Builder().forBrowser("chrome").build();

  try {
    // Navigate to login page
    await driver.get("http://localhost:3000/peoples_budget/login");
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // // Click on the "State Budget - 2022" button
    // await driver.findElement(By.id("budgetBtn")).click();
    // await new Promise((resolve) => setTimeout(resolve, 5000));
    // await driver.findElement(By.id("budgetBtn")).click();

    // Enter login credentials
    await driver.findElement(By.id("logId")).sendKeys("315315315");
    await new Promise((resolve) => setTimeout(resolve, 1500));
    await driver
      .findElement(By.id("logPassword"))
      .sendKeys("315315", Key.RETURN);
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Navigate to Home page
    await driver.findElement(By.id("loginBtn")).click();

    // Wait for login to complete
    await driver.wait(
      until.urlIs("http://localhost:3000/peoples_budget/home"),
      2000
    );

    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Verify successful login
    let title = await driver.getTitle();
    if (title === "Home") {
      console.log("------------ Login test passed ------------");
    } else {
      console.log("------------ Login test failed ------------");
    }
    await new Promise((resolve) => setTimeout(resolve, 2000));
  } finally {
    await driver.quit();
  }
};

module.exports = LoginTests;
