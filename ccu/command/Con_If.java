package ccu.command;

import java.util.ArrayList;

import ccu.general.ArgUtils;
import ccu.general.NumberUtils;
import ccu.general.StringUtils;

public class Con_If {
	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;

	public Con_If(ArrayList<String> arrayGet, int tabNumGet, String fullLineGet) {
		this.arrayGet = arrayGet;
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {
		/** Essentially runs the given array if the arguments return true
		 * The majority of that will be parsed in the MathParser class
		 * 
		 * To tone it down a bit, OR / AND will not be included (maybe later, but not now since that's too insane for me atm)
		 * It will simply be seperated by =, >, <, >=, <= or only = if not numbers
		 */

		Boolean foundOperator = null;
		String getOperator = null;
		String[] splitArgsCalc = null;
		String[] splitArgsTemp = new String[2];
		double[] splitArgsDouble = new double[2];
		Boolean calcStatement = null;

		final String[] operatorArray = {">=", "<=", ">", "<", "!=", "="};

		// Removes "IF" and isolates for the arguments with brackets
		String statementEncase = this.fullLineGet.replaceFirst("IF", "").replaceAll("^\\s+", "");
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}:")) {
			String statementArgs = statementEncase.substring(1, statementEncase.length() - 2);

			for (String operator : operatorArray) {
				if (statementArgs.contains(operator)) {

					if (foundOperator == null) { // checks multiple different operators
						foundOperator = true;
						getOperator = operator;

						// checks for multiple of the same operataors
						if (StringUtils.countChars(statementArgs, operator) > 1) {
							System.out.println("ERROR: Two conflicting operators ('" + operator + "' and '" + operator
									+ "') have been found in line '" + this.fullLineGet + "'");
							System.exit(0);
						}

						break;
					} else {
						System.out.println("ERROR: Two conflicting operators ('" + getOperator + "' and '" + operator
								+ "') have been found in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
				}
			}

			if (foundOperator == false) {
				System.out.println("ERROR: An operator for '" + this.fullLineGet + "' has not been found");
				System.exit(0);
			}

			// gets the actual numeric values on each side
			splitArgsCalc = statementArgs.split(getOperator);

			for (int i = 0; i < 2; i++) {

				// removes excess whitespace
				splitArgsCalc[i] = splitArgsCalc[i].trim();

				// gets 'NULL' --> nothing
				if (splitArgsCalc[i].equals("NULL")) {
					splitArgsCalc[i] = "";
				}

				splitArgsCalc[i] = MathParser.parseSecondaryStatements(splitArgsCalc[i], this.fullLineGet);
				splitArgsTemp[i] = MathParser.getOperation(splitArgsCalc[i], this.fullLineGet, false, 0);
			}

			// is number
			if (NumberUtils.isNum(splitArgsTemp[0]) && NumberUtils.isNum(splitArgsTemp[1])) {

				splitArgsDouble[0] = Double.parseDouble(splitArgsTemp[0]);
				splitArgsDouble[1] = Double.parseDouble(splitArgsTemp[1]);

				// calculates whether it should accept the array or not (with calcStatement)
				switch (getOperator) {
				case "=":
					if (splitArgsDouble[0] == splitArgsDouble[1]) {
						calcStatement = true;
					} else {
						calcStatement = false;
					}
					break;

				case "<":
					if (splitArgsDouble[0] < splitArgsDouble[1]) {
						calcStatement = true;
					} else {
						calcStatement = false;
					}
					break;

				case ">":
					if (splitArgsDouble[0] > splitArgsDouble[1]) {
						calcStatement = true;
					} else {
						calcStatement = false;
					}
					break;

				case "<=":
					if (splitArgsDouble[0] <= splitArgsDouble[1]) {
						calcStatement = true;
					} else {
						calcStatement = false;
					}
					break;

				case ">=":
					if (splitArgsDouble[0] >= splitArgsDouble[1]) {
						calcStatement = true;
					} else {
						calcStatement = false;
					}
					break;

				case "!=":
					if (splitArgsDouble[0] != splitArgsDouble[1]) {
						calcStatement = true;
					} else {
						calcStatement = false;
					}
					break;
				}

			} else { // if string
				if (getOperator.equals("=")) {
					if (splitArgsTemp[0].equals(splitArgsTemp[1])) {
						calcStatement = true;
					} else {
						calcStatement = false;
					}
				} else {
					if (getOperator.equals("!=")) {
						if (splitArgsTemp[0].equals(splitArgsTemp[1])) {
							calcStatement = false;
						} else {
							calcStatement = true;
						}
					} else {
						System.out.println("ERROR: Operator '" + getOperator + "' for comparing string is not recognized for line '"
								+ this.fullLineGet + "'");
						System.exit(0);
					}
				}
			}

			// checks if calcStatement is null --> aka fail
			if (calcStatement == null) {
				System.out.println("ERROR: I have literally no idea how you got here but there's something wrong with line '"
						+ this.fullLineGet + "' and that's all I can tell you");
				System.exit(0);
			}

			// To prevent lag, checkCommands() is done ONLY after the first part of the IF command returns true
			if (calcStatement == true) {
				ArgUtils.checkCommands(this.arrayGet, tabNum);

				// gets rid of tab spaces
				for (int i = 0; i < this.arrayGet.size(); i++) {
					this.arrayGet.set(i, this.arrayGet.get(i).substring(1));
				}

				return this.arrayGet;
			} else {
				return null;
			}

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		// if you reach here, idk what to do anymore >_>
		return null;
	}
}
