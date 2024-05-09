// Importing the necessary test files
const HeaderTests = require('./HeaderTests');
const InfoTests = require('./InfoTests');
const SignupTests = require('./SignupTests');
const LoginTests = require('./LoginTests');
const NavTests = require('./NavTests');
const ResultsTests = require('./ResultsTests');
const VotingTests = require('./VotingTests');

// Get the test file name from command-line argument
const testFile = process.argv[2];

// Function to run a specific test file
async function runTestFile(testFunction) {
  console.log(`Running ${testFile}...`);
  await testFunction();
}

// Running the selected test file or all tests if no specific file is specified
async function runAllTests() {
  if (testFile === "HeaderTests") {
    await runTestFile(HeaderTests);
  } else if (testFile === "InfoTests") {
    await runTestFile(InfoTests);
  } else if (testFile === "SignupTests") {
    await runTestFile(SignupTests);
  } else if (testFile === "LoginTests") {
    await runTestFile(LoginTests);
  } else if (testFile === "NavTests") {
    await runTestFile(NavTests);
  } else if (testFile === "ResultsTests") {
    await runTestFile(ResultsTests);
  } else if (testFile === "VotingTests") {
    await runTestFile(VotingTests);
  } else {
    // Run all tests if no specific test file is specified
    await runTestFile(HeaderTests);
    await runTestFile(InfoTests);
    await runTestFile(SignupTests);
    await runTestFile(LoginTests);
    await runTestFile(NavTests);
    await runTestFile(ResultsTests);
    await runTestFile(VotingTests);
  }
}

// Invoke the function to start running the tests
runAllTests();
