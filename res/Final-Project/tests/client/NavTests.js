const { Builder, By, until } = require("selenium-webdriver");

async function NavTests() {
  let driver = await new Builder().forBrowser("chrome").build();

  try {
    // Navigate to Login page
    await driver.get("http://localhost:3000/peoples_budget/login");
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Navigate to Home page
    await driver.findElement(By.id("loginGuest")).click();

    await new Promise((resolve) => setTimeout(resolve, 3200));

    // Navigate to Voting page
    let votingLink = await driver.wait(
      until.elementLocated(By.linkText("Voting")),
      10000
    );
    await votingLink.click();
    await new Promise((resolve) => setTimeout(resolve, 2500));

    // Wait for page to load
    await driver.wait(
      until.urlIs("http://localhost:3000/peoples_budget/voting"),
      10000
    );

    // Verify navigation to Voting page
    title = await driver.getTitle();
    if (title !== "Voting") {
      console.log(
        "------------ Voting page navigation test failed ------------"
      );
    } else {
      console.log(
        "------------ Voting page navigation test passed ------------"
      );
    }

    // Navigate to Information page
    await driver.findElement(By.linkText("Information")).click();
    await new Promise((resolve) => setTimeout(resolve, 2500));

    // Wait for page to load
    await driver.wait(
      until.urlIs("http://localhost:3000/peoples_budget/information"),
      10000
    );

    // Verify navigation to Information page
    title = await driver.getTitle();
    if (title !== "Information") {
      console.log(
        "------------ Information page navigation test failed ------------"
      );
    } else {
      console.log(
        "------------ Information page navigation test passed ------------"
      );
    }

    // Navigate to Dashboard page
    await driver.findElement(By.linkText("Dashboard")).click();
    await new Promise((resolve) => setTimeout(resolve, 2500));

    // Wait for page to load
    await driver.wait(
      until.urlIs("http://localhost:3000/peoples_budget/dashboard"),
      10000
    );

    // Verify navigation to Dashboard page
    title = await driver.getTitle();
    if (title !== "Dashboard") {
      console.log(
        "------------ Dashboard page navigation test failed ------------"
      );
    } else {
      console.log(
        "------------ Dashboard page navigation test passed ------------"
      );
    }

    // Navigate to Results page
    await driver.findElement(By.linkText("Results")).click();
    await new Promise((resolve) => setTimeout(resolve, 5000));

    // Wait for page to load
    await driver.wait(
      until.urlIs("http://localhost:3000/peoples_budget/results"),
      10000
    );

    // Verify navigation to Results page
    title = await driver.getTitle();
    if (title !== "Results") {
      console.log(
        "------------ Results page navigation test failed ------------"
      );
    } else {
      console.log(
        "------------ Results page navigation test passed ------------"
      );
    }

    // Navigate to Home page
    await driver.findElement(By.linkText("Home")).click();
    await new Promise((resolve) => setTimeout(resolve, 2500));

    // Wait for page to load
    await driver.wait(
      until.urlIs("http://localhost:3000/peoples_budget/home"),
      10000
    );

    // Verify navigation to Home page
    title = await driver.getTitle();
    if (title !== "Home") {
      console.log("------------ Home page navigation test failed ------------");
    } else {
      console.log("------------ Home page navigation test passed ------------");
    }
  } finally {
    await driver.quit();
  }
};

module.exports = NavTests;
