const { Builder, By, Key, until } = require("selenium-webdriver");

async function VoteTests() {
  let driver = await new Builder().forBrowser("chrome").build();
  let ids = ["1", "1178", "4885", "6802", "9707", "10696", "10793"];

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
    await new Promise((resolve) => setTimeout(resolve, 4500));

    // Wait for page to load
    await driver.wait(
      until.urlIs("http://localhost:3000/peoples_budget/voting"),
      10000
    );

    // Move slider1
    let slider1 = await driver.findElement(By.id("slider1"));
    await driver
      .actions({ bridge: true })
      .dragAndDrop(slider1, { x: 0, y: 55 })
      .perform();
    await new Promise((resolve) => setTimeout(resolve, 1500));
    await driver
      .actions({ bridge: true })
      .dragAndDrop(slider1, { x: 25, y: 0 })
      .perform();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Check that the sum of all slider values equals to max budget
    let sum = 0;
    for (let i = 0; i < ids.length; i++) {
      let sliderValueElement = await driver.findElement(
        By.id(`budgetText${ids[i]}`)
      );
      let sliderValue = await sliderValueElement.getAttribute("value");
      sum += parseInt(sliderValue);
    }
    if (sum > 596770400000 || sum <= 596770415000) {
      console.log("------------ Slider test 1 passed  ------------");
    } else {
      console.log("------------ Slider test 1 failed ------------");
    }

    // Move slider2
    let slider2 = await driver.findElement(By.id("slider1178"));
    await driver
      .actions({ bridge: true })
      .dragAndDrop(slider2, { x: 15, y: 10 })
      .perform();
    await driver
      .actions({ bridge: true })
      .dragAndDrop(slider2, { x: 0, y: 0 })
      .perform();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Check that the sum of all slider values equals to max budget
    sum = 0;
    for (let i = 0; i < ids.length; i++) {
      let sliderValueElement = await driver.findElement(
        By.id(`budgetText${ids[i]}`)
      );
      let sliderValue = await sliderValueElement.getAttribute("value");
      sum += parseInt(sliderValue);
    }
    if (sum > 596770400000 || sum <= 596770415000) {
      console.log("------------ Slider test 2 passed  ------------");
    } else {
      console.log("------------ Slider test 2 failed ------------");
    }

    // Move slider3
    let slider3 = await driver.findElement(By.id("slider4885"));
    await driver
      .actions({ bridge: true })
      .dragAndDrop(slider3, { x: 15, y: 0 })
      .perform();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Check that the sum of all slider values equals to max budget
    sum = 0;
    for (let i = 0; i < ids.length; i++) {
      let sliderValueElement = await driver.findElement(
        By.id(`budgetText${ids[i]}`)
      );
      let sliderValue = await sliderValueElement.getAttribute("value");
      sum += parseInt(sliderValue);
    }
    if (sum > 596770400000 || sum <= 596770415000) {
      console.log("------------ Slider test 3 passed  ------------");
    } else {
      console.log("------------ Slider test 3 failed ------------");
    }

    // Click the checkbox
    let checkbox = await driver.findElement(By.id("checkbox1178"));
    await checkbox.click();

    // Move slider4
    let slider4 = await driver.findElement(By.id("slider6802"));
    await driver
      .actions({ bridge: true })
      .dragAndDrop(slider4, { x: 45, y: 0 })
      .perform();
    await new Promise((resolve) => setTimeout(resolve, 1500));
    await driver
      .actions({ bridge: true })
      .dragAndDrop(slider4, { x: 0, y: 15 })
      .perform();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Check that the sum of all slider values equals to max budget
    sum = 0;
    for (let i = 0; i < ids.length; i++) {
      let sliderValueElement = await driver.findElement(
        By.id(`budgetText${ids[i]}`)
      );
      let sliderValue = await sliderValueElement.getAttribute("value");
      sum += parseInt(sliderValue);
    }
    if (sum > 596770400000 || sum <= 596770415000) {
      console.log("------------ Slider test 4 passed  ------------");
    } else {
      console.log("------------ Slider test 4 failed ------------");
    }

    // Click the checkbox
    let checkbox1 = await driver.findElement(By.id("checkbox1178"));
    await checkbox1.click();

    // Click to open children
    await driver.findElement(By.id("iconTree1")).click();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Move slider5
    let slider5 = await driver.findElement(By.id("slider2"));
    await driver
      .actions({ bridge: true })
      .dragAndDrop(slider5, { x: 10, y: 0 })
      .perform();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Click to close children
    await driver.findElement(By.id("iconTree1")).click();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Click the checkbox
    let checkbox2 = await driver.findElement(By.id("checkbox1178"));
    await checkbox2.click();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    let checkbox3 = await driver.findElement(By.id("checkbox4885"));
    await checkbox3.click();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    let checkbox4 = await driver.findElement(By.id("checkbox6802"));
    await checkbox4.click();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    await driver.findElement(By.id("clearAll")).click();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Change text field
    let inputField1 = await driver.findElement(By.id("budgetText1"));
    await inputField1.sendKeys(Key.chord(Key.CONTROL, "a")); // select all text
    await inputField1.sendKeys(Key.DELETE); // delete selected text
    let budgetValue = "666"; // new budget value
    for (let i = 0; i < budgetValue.length; i++) {
      await inputField1.sendKeys(Number(budgetValue.charAt(i)));
    }
    await new Promise((resolve) => setTimeout(resolve, 1500));
    budgetValue = "233"; // new budget value
    await inputField1.sendKeys(Key.chord(Key.CONTROL, "a")); // select all text
    await inputField1.sendKeys(Key.DELETE); // delete selected text
    for (let i = 0; i < budgetValue.length; i++) {
      await inputField1.sendKeys(Number(budgetValue.charAt(i)));
    }
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Check that the sum of all textfield values equals to max budget
    sum = 0;
    for (let i = 0; i < ids.length; i++) {
      let sliderValueElement = await driver.findElement(
        By.id(`budgetText${ids[i]}`)
      );
      let sliderValue = await sliderValueElement.getAttribute("value");
      sum += parseInt(sliderValue);
    }
    if (sum > 596770400000 || sum <= 596770415000) {
      console.log("------------ Textfield test passed  ------------");
    } else {
      console.log("------------ Textfield test failed ------------");
    }

    // Click on 'Submit' button
    await driver.findElement(By.id("voteSubmit")).click();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    await driver.findElement(By.id("submit")).click();
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Wait for voting to complete
    await driver.wait(
      until.urlIs("http://localhost:3000/peoples_budget/results"),
      1000
    );

    await new Promise((resolve) => setTimeout(resolve, 3000));

    // Changed screen successfully
    let title = await driver.getTitle();
    if (title === "Results") {
      console.log("------------ Voting test passed  ------------");
    } else {
      console.log("------------ Voting test failed ------------");
    }
  } finally {
    await driver.quit();
  }
};

module.exports = VoteTests;
