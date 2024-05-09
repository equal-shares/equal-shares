const { Builder, By, Key, until } = require("selenium-webdriver");

async function SignupTests() {
  let driver = await new Builder().forBrowser("chrome").build();

  try {
    // Navigate to signup page
    await driver.get("http://localhost:3000/peoples_budget/sign_up");
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Enter signup details
    await driver.findElement(By.id("fName")).sendKeys("Eli");
    await new Promise((resolve) => setTimeout(resolve, 500));
    await driver.findElement(By.id("lName")).sendKeys("Levy");
    await new Promise((resolve) => setTimeout(resolve, 500));
    await driver.findElement(By.id("signId")).sendKeys("359159179");
    await new Promise((resolve) => setTimeout(resolve, 500));
    await driver.findElement(By.id("date")).sendKeys("03/06/1999");
    await new Promise((resolve) => setTimeout(resolve, 500));
    await driver.findElement(By.id("gender")).click();
    await new Promise((resolve) => setTimeout(resolve, 500));
    await driver.findElement(By.css("li[data-value='male']")).click();
    await new Promise((resolve) => setTimeout(resolve, 500));
    await driver.findElement(By.id("email")).sendKeys("eli113@gmail.com");
    await new Promise((resolve) => setTimeout(resolve, 500));
    await driver
      .findElement(By.id("signPassword"))
      .sendKeys("Pass123", Key.RETURN);
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Navigate to Home page
    await driver.findElement(By.id("signBtn")).click();
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Wait for signup to complete
    await driver.wait(
      until.urlIs("http://localhost:3000/peoples_budget/login"),
      10000
    );

    // Verify successful signup
    let title = await driver.getTitle();
    if (title === "Login") {
      console.log("------------ Signup test passed ------------");
    } else {
      console.log("------------ Signup test failed ------------");
    }

    await new Promise((resolve) => setTimeout(resolve, 2000));
  } finally {
    await driver.quit();
  }
};

module.exports = SignupTests;
