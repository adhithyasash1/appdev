/*
 * calculateSimpleInterest calculates and returns the simple interest
 * (floor value) for a fixed deposit. Formula used is,

 * calculateSimpleInterest calculates and returns the simple interest
 * for a fixed deposit. Formula used is,
 * Simple Interest: P X R X T / 100
 *   where:
 *   P = Principal
 *   I = Daily interest rate
 *   N = Number of days
 *
 *  In case of any input error (wrong date format, alphabets in daily interest etc.), return -1
 *
 * @param {number} principal  - Principal amount
 * @param {number} dailyInterest  - daily interest rate
 * @param {string} startingDate  - Starting date of the fixed deposit in "YYYY-MM-DD" format, example "2015-03-25"
 * @param {string} endingDate  - Ending date of the fixed deposit in "YYYY-MM-DD" format, example "2015-03-25"
 * @return {number} interest
*/

/*
 * calculateCompoundInterest calculates and returns the compound interest
 * (floor value) for a fixed deposit. Formula used is,
 *   Compound Interest=P[(1+I/100)^N - 1]
 *   where:
 *   P = Principal
 *   I = Daily interest rate
 *   N = Number of days
 *
 *  In case of any input error (wrong date format, alphabets in daily interest etc.), return -1
 *
 * @param {number} principal  - Principal amount
 * @param {number} dailyInterest  - daily interest rate
 * @param {string} startingDate  - Starting date of the fixed deposit in "YYYY-MM-DD" format, example "2015-03-25"
 * @param {string} endingDate  - Ending date of the fixed deposit in "YYYY-MM-DD" format, example "2015-03-25"
 * @return {number} interest
*/

/*
 * extraAmountPercentage calculates and returns the extra amount percentage borrower will have to pay in case of
 * compound interest (floor value) in comparison to the simple interest for a fixed deposit.

 *  In case of any input error (wrong date format, alphabets in daily interest etc.), return -1
 *
 * @param {number} principal  - Principal amount
 * @param {number} dailyInterest  - Daily interest rate.
 * @param {string} startingDate  - Starting date of the fixed deposit in "YYYY-MM-DD" format, example "2015-03-25"
 * @param {string} endingDate  - Ending date of the fixed deposit in "YYYY-MM-DD" format, example "2015-03-25"
 * @return {number} percentage
*/
function calculateSimpleInterest(
  principal,
  dailyInterest,
  startingDate,
  endingDate
) {

s = new Date(startingDate);
e = new Date(endingDate);
//console.log(s, "\n", e);
if (s == "Invalid Date") {return -1;}
if (e == "Invalid Date") {return -1;}
diff = (e.getTime() - s.getTime()) / (1000 * 60 * 60 * 24);

result = Number(principal) * Number(dailyInterest) * Number(diff) / 100;
return Math.floor(result);

}

function calculateCompoundInterest(
  principal,
  dailyInterest,
  startingDate,
  endingDate
) {
    
s = new Date(startingDate);
e = new Date(endingDate);
if (s == "Invalid Date") {return -1;}
if (e == "Invalid Date") {return -1;}

diff = (e.getTime() - s.getTime()) / (1000 * 60 * 60 * 24);

result = principal * (Math.pow((1 + dailyInterest / 100), diff) - 1);
    
return Math.floor(result);
}

function extraAmountPercentage(principal, dailyInterest, startingDate, endingDate) {
    
    compound = calculateCompoundInterest(
  principal,
  dailyInterest,
  startingDate,
  endingDate
);
    simple = calculateSimpleInterest(
  principal,
  dailyInterest,
  startingDate,
  endingDate
);
if (compound == -1) {return -1;}
if (simple == -1) {return -1;}
    return Math.floor((compound - simple) / simple * 100);
}
