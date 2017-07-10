package ccu.command;

import java.util.ArrayList;
import java.util.regex.Pattern;

import ccu.general.ArgUtils;
import ccu.general.GeneralFile;
import ccu.general.StringUtils;

public class Cmd_MFunc {

	// The actual commands
	public static ArrayList<String[]> arrayMFuncSave = new ArrayList<String[]>();

	// Nickname
	public static ArrayList<String> arrayMFuncNameSave = new ArrayList<String>();

	// File name calc via branch
	public static ArrayList<String> fileMFuncBranchSave = new ArrayList<String>();

	// Tab number calc via branch
	public static ArrayList<Integer> fileMFuncTabnumSave = new ArrayList<Integer>();

	// Calculating the name for the /function command
	public static ArrayList<String> fileMFuncCommandSave = new ArrayList<String>();

	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;
	private String branchCalc = null;

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
		 * 	MFUNC {BRANCH french_man/asdf AyyLmao Nickname}:
		 * that means all including AyyLmao nickname is going to be within the branch
		 */

		// Removes "MFUNC" and isolates for the arguments with brackets
		String statementEncase = this.fullLineGet.replaceFirst("MFUNC", "").replaceAll("^\\s+", "");
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}:")) {
			String statementArgs = statementEncase.substring(1, statementEncase.length() - 2);

			// Calculates fileMFuncNameSave - if there are any that are the same tab num, is removed
			int calcTabNum = 0;
			while (calcTabNum < fileMFuncBranchSave.size()) {
				if (fileMFuncTabnumSave.get(calcTabNum) >= tabNum) {
					fileMFuncTabnumSave.remove(calcTabNum);
					fileMFuncBranchSave.remove(calcTabNum);
				} else {
					calcTabNum++;
				}
			}

			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "BRANCH":
					// removes BRANCH
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);

					if (statementArgs.contains(" ") == false) {
						System.out.println("ERROR: Invalid parameters for 'BRANCH' in line '" + this.fullLineGet + "'");
						System.exit(0);
					}

					// adds to the array for calculations
					fileMFuncBranchSave.add(statementArgs.substring(0, statementArgs.indexOf(" ")));
					fileMFuncTabnumSave.add(tabNum);

					// removes the file name
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);

					break;
				}
			}

			// Calculates for the BRANCH keyword
			if (fileMFuncBranchSave.size() > 0) {
				// branchCalc fileMFuncCommandSave
				for (int i = 0; i < fileMFuncBranchSave.size(); i++) {
					if (i == 0) {
						branchCalc = Var_Options.filePathFuncOption.toString() + "/" + fileMFuncBranchSave.get(i);
					} else {
						branchCalc += "/" + fileMFuncBranchSave.get(i);
					}
				}
			}

			// Sees if there's a nickname
			if (statementArgs.contains(" ")) {
				arrayMFuncNameSave.add(statementArgs.substring(statementArgs.indexOf(" ") + 1));
				branchCalc += "/" + statementArgs.substring(0, statementArgs.indexOf(" "));

			} else {
				arrayMFuncNameSave.add("");
				branchCalc += "/" + statementArgs;
			}

			// replaces all \ with /
			branchCalc = branchCalc.replace("\\", "/");

			// test for any duplicate names for all function nicknames
			for (int i = 0; i < arrayMFuncNameSave.size(); i++) {
				for (int j = 0; j < arrayMFuncNameSave.size(); j++) {
					if (i != j && arrayMFuncNameSave.get(i).equals(arrayMFuncNameSave.get(j))) {
						System.out.println("ERROR: '" + arrayMFuncNameSave.get(j)
								+ "' is repeated as a MFunc nickname detected in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
				}
			}

			/* spellchecks for the file extension
			 * if file is asdf.notmcfunction
			 * 	-removes .notmcfunction and replaces it with .mcfunction
			 *  -displays WARNING
			 * if file is asdf
			 *  -adds .mcfunction
			 * if file is asdf.mcfunction
			 *  -does nothing woot woot
			 */

			branchCalc = GeneralFile.checkFileExtension(branchCalc, ".mcfunction");

			System.out.println("File created: '" + branchCalc + "'");

			// Gets replacement for definitions via fileMFuncCommandSave
			// if there is no '\functions\' file, you ded af
			if (branchCalc.contains("/functions/")) {
				Cmd_MFunc.fileMFuncCommandSave.add(branchCalc.substring(0, branchCalc.length() - 11)
						.substring(branchCalc.indexOf("/functions/") + 11).replaceFirst(Pattern.quote("/"), ":"));
			} else {
				System.out.println("ERROR: '" + branchCalc + "' is not in a 'functions' folder");
				System.exit(0);
			}

			// readCommands() recurring method is done down here because the beginning arguments must be gotten first
			ReadCCUFile ccuSubsetFile = new ReadCCUFile(this.arrayGet, tabNum);
			ArrayList<String> checkCommandsArray = ccuSubsetFile.checkCommands();
			if (checkCommandsArray != null && checkCommandsArray.isEmpty() == false) {
				this.arrayGet = checkCommandsArray;
			}

			// Creates the string array, and puts it in the arraylist
			// Notice how the first element in each array is the mfunc name and not a valid command
			String[] arrayMFunc = new String[this.arrayGet.size() + 1];
			arrayMFunc[0] = branchCalc;

			// checks tab spaces
			ArgUtils.checkWhiteSpace(this.arrayGet, this.tabNum);

			for (int i = 0; i < this.arrayGet.size(); i++) {
				// Check if "CCU_COND_" is in the front
				if (this.arrayGet.get(i).replaceAll("^\\s+", "").length() >= 9
						&& this.arrayGet.get(i).replaceAll("^\\s+", "").substring(0, 9).equals("CCU_COND_")) {
					System.out.println("ERROR: 'COND:' is an invalid argument inside 'MFUNC' (starting at line '"
							+ this.arrayGet.get(i).replace("CCU_COND_", "") + "'");
					System.exit(0);
				}

				arrayMFunc[i + 1] = StringUtils.generalParse(this.arrayGet.get(i).trim());
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
		return null;
	}
}
