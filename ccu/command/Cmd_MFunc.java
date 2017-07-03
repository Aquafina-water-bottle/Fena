package ccu.command;

import java.util.ArrayList;

public class Cmd_MFunc {
	public static ArrayList<String[]> arrayMFuncSave = new ArrayList<String[]>();
	public static ArrayList<String> arrayMFuncNameSave = new ArrayList<String>();

	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;

	public Cmd_MFunc(ArrayList<String> arrayGet, int tabNumGet, String fullLineGet) {
		this.arrayGet = arrayGet;
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {
		/** MFUNC
		 * This mostly just gets the name in the curly brackets, checks for more
		 * statements, and then puts the commands in an array and returns null
		 * 
		 * Arguments:
		 * BRANCH - only 
		 *  -done by seperate array to concatenate all branch listed names
		 * Using BRANCH-
		 * 	MFUNC {BRANCH french_man/asdf} {AyyLmao Nickname}:
		 */

		//System.out.println("LINE " + fullLineGet);

		ReadCCUFile ccuSubsetFile = new ReadCCUFile(this.arrayGet, tabNum);
		ArrayList<String> checkCommandsArray = ccuSubsetFile.checkCommands();
		if (checkCommandsArray != null && checkCommandsArray.isEmpty() == false) {
			this.arrayGet = checkCommandsArray;
		}

		// Removes "MFUNC " and isolates for the arguments with brackets
		String statementEncase = this.fullLineGet.replaceFirst("MFUNC", "").replaceAll("^\\s+", "");
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}:")) {
			String statementArgs = statementEncase.substring(1, statementEncase.length() - 2);

			// Creates the string array, and puts it in the arraylist
			// Notice how the first element in each array is the group name and not a valid command
			String[] arrayMFunc = new String[this.arrayGet.size() + 1];
			arrayMFunc[0] = statementArgs;
			for (int i = 0; i < this.arrayGet.size(); i++) {

				// Checking tab spaces
				String whitespaceCalc = this.arrayGet.get(i).substring(0,
						(this.arrayGet.get(i).length() - this.arrayGet.get(i).replaceAll("^\\s+", "").length()));
				if (whitespaceCalc.contains(" ")) {
					System.out.println(
							"ERROR: Line '" + this.arrayGet.get(i) + "' contains spaces instead of tab spaces");
					System.exit(0);
				}

				if (whitespaceCalc.length() - whitespaceCalc.replace("\t", "").length() != this.tabNum) {
					System.out.println(
							"ERROR: Line '" + this.arrayGet.get(i) + "' contains an incorrect number of tab spaces");
					System.exit(0);
				}

				// Check if "CCU_COND_" is in the front
				if (this.arrayGet.get(i).replaceAll("^\\s+", "").length() >= 9
						&& this.arrayGet.get(i).replaceAll("^\\s+", "").substring(0, 9).equals("CCU_COND_")) {
					System.out.println("ERROR: 'COND:' is an invalid argument inside 'MFUNC' (starting at line '"
							+ this.arrayGet.get(i).replace("CCU_COND_", "") + "'");
					System.exit(0);
				}

				arrayMFunc[i + 1] = this.arrayGet.get(i).replaceAll("^\\s+", "");
			}

			arrayMFuncSave.add(arrayMFunc);

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		// test for any duplicate names for all function names
		for (int i = 0; i < arrayMFuncSave.size(); i++) {
			for (int j = 0; j < arrayMFuncSave.size(); j++) {
				if (i != j && arrayMFuncSave.get(i)[0].equals(arrayMFuncSave.get(j)[0])) {
					System.out.println("ERROR: '" + arrayMFuncSave.get(j)[0] + "' is repeated as a MFunc name");
					System.exit(0);
				}
			}
		}

		// should always return null
		return null;
	}
}
