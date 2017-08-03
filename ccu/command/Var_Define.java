package ccu.command;

import java.util.ArrayList;

import ccu.general.ArgUtils;
import ccu.general.NumberUtils;
import ccu.general.ParamUtils;

public class Var_Define {
	public static ArrayList<String[]> arrayDefineSave = new ArrayList<String[]>();

	private int tabNum;
	private String fullLineGet;

	public Var_Define(String fullLineGet, int tabNumGet) {
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	// list of definitions that CANNOT be definitions because they are used for parameters for other CCU statements
	// if 3, dy / dx returns ~
	// if 4, dx returns ~
	// Add seperation of numbers via ;

	// @formatter:off
	public static String[] exceptionArray = {
			"DEF", "ARRAY", "SET", "SPLIT", "GLOBAL", "COORDS", "TELE", 
			"GROUP", "PULSE", "CLOCK", "BLOCK",
			"USE", "BEG", "END", "NOSPACE",
			"FUNC", "ACTIVATE", "CALL", 
			"MFUNC", "BRANCH",
			"IMPORT", "LIBRARY", "GETDIR", "WITHIN", "GETCOORDS", 
			"CALC", "SIN", "COS", "TAN", "INT", "DOUBLE", "GSELF",
			"COND", "OPTIONS", "UNASSIGN", "IF", "ELSE", "ELIF", "LOOP", "PRINT", "INITIALIZE", "FINALIZE"
			};
	// @formatter:on

	public ArrayList<String> getArray() {
		/** Defines are generally a find --> replace thing
		 * Normal:
		 * DEF $Test$ asdf
		 * GLOBAL can be added to affect all and not just within the encapsulation
		 * COORDS --> set of 3, 4, 5 or 6 numbers
		 * 
		 * TODO
		 * If COORDS --> name[x] gets x, name[y] gets y, name[z] gets z
		 */

		/* arrayDefineCalc will include:
		 * 	-Definition type - defineType
		 *  -tabNum - tabNum
		 *  -name - defineName
		 * 	-string - defintionGet
		 */
		String[] arrayDefineCalc = new String[5];
		Integer defineType = null;
		Boolean isGlobal = null;

		String defineName = null;
		String defintionGet = null;
		int paramMaxNum = 0;

		/* defineType
		 * null = unspecified, will be specified after
		 * 0 = NULL
		 * 1 = string
		 * 4 = coords
		 * 5 = teleport
		 */

		// Removes "DEF" and for all arguments

		// Checks tab spaces
		ArgUtils.checkWhiteSpace(this.fullLineGet, this.tabNum);

		String statementEncase = this.fullLineGet.replaceFirst("DEF", "").replaceAll("^\\s+", "");
		switch (statementEncase.substring(0, statementEncase.indexOf(" "))) {
		case "GLOBAL":
			isGlobal = true;
			// removes GLOBAL
			statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1);
			break;
			
		case "COORDS":
			defineType = 4;
			// removes COORDS
			statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1);
			break;

		case "TELE":
			defineType = 5;
			// removes COORDS
			statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1);
			break;
		}

		// Gets second parameters
		if (statementEncase.contains(" ")) {
			switch (statementEncase.substring(0, statementEncase.indexOf(" "))) {
			case "GLOBAL":
				if (isGlobal == null) {
					isGlobal = true;
				} else {
					System.out.println(
							"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
				// removes GLOBAL
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1, statementEncase.length());
				break;
				
			case "COORDS":
				if (defineType == null) {
					defineType = 4;
				} else {
					System.out.println(
							"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
				// removes COORDS
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1, statementEncase.length());
				break;

			case "TELE":
				if (defineType == null) {
					defineType = 5;
				} else {
					System.out.println(
							"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
				// removes COORDS
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1, statementEncase.length());
				break;
			}
			// the end should make 'statementEncase' as the actual use thing (Name Definition)

			// Sets name
			if (statementEncase.contains(" ")) {
				defineName = statementEncase.substring(0, statementEncase.indexOf(" "));
				defintionGet = statementEncase.substring(statementEncase.indexOf(" ") + 1, statementEncase.length());

				// Checks if defineName is literally nothing
				if (defineName.trim().length() == 0) {
					System.out.println("ERROR: Definition '" + this.fullLineGet + "' is blank");
					System.exit(0);
				}

				// Checks if the name matches any unacceptable define names
				for (String checkException : exceptionArray) {
					if (defineName.equals(checkException)) {
						System.out.println("ERROR: A definition cannot be '" + defineName + "' in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
				}

				// Checks how many parameters exist
				paramMaxNum = ParamUtils.countParams(defintionGet);

			} else {
				System.out.println("ERROR: '" + this.fullLineGet + "' does not define anything without spaces");
				System.exit(0);
			}

			// sets options if they are unspecified
			if (isGlobal == null) {
				isGlobal = false;
			}
			// detects definition type if not specified

			/*
			if (defineType == null) {
				if (NumberUtils.isInt(defintionGet)) {
					// is int
					defineType = 2;
				}
			
				if (NumberUtils.isDouble(defintionGet)) {
					// is double
					defineType = 3;
				}
			}*/

			// Sets to string
			if (defineType == null) {
				defineType = 1;
			}

			// tests whether coords works
			ArgUtils.checkCoords(defintionGet, defineType, this.fullLineGet);

			// If global, tabnum = 0
			if (isGlobal == true) {
				this.tabNum = 0;
			}

			arrayDefineCalc[0] = defineType.toString();
			arrayDefineCalc[1] = tabNum + "";
			arrayDefineCalc[2] = defineName;
			arrayDefineCalc[3] = defintionGet;

			// System.out.println("LOOKUP " + defintionGet);

			arrayDefineCalc[4] = paramMaxNum + "";

			// Checks whether the defineName and tabnum is the same anywhere --> will remove
			int defIndex = 0;
			while (defIndex < arrayDefineSave.size()) {
				if (arrayDefineSave.get(defIndex)[2].equals(defineName) && arrayDefineSave.get(defIndex)[1].equals(tabNum + "")) {
					arrayDefineSave.remove(defIndex);
				} else {
					defIndex++;
				}
			}

			arrayDefineSave.add(arrayDefineCalc);

			// System.out.println(arrayDefineCalc[2] + " | " + arrayDefineCalc[1]);
		}
		return null;
	}

	// This is used specifically for getting the part past the definition name
	// There cannot be a definition in replacement for 'GLOBAL' or 'TELE' or 'COORDS'
	public static int getDefineIndex(String getLine) {
		String statementEncase = getLine.replaceFirst("DEF", "").replaceAll("^\\s+", "");
		String statementEncaseCalc = null;

		if (statementEncase.contains(" ")) {
			statementEncaseCalc = statementEncase.substring(0, statementEncase.indexOf(" "));
			if (statementEncaseCalc.equals("GLOBAL") || statementEncaseCalc.equals("TELE") || statementEncaseCalc.equals("COORDS")) {
				// removes keyword
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1, statementEncase.length());
			}
		}

		if (statementEncase.contains(" ")) {
			statementEncaseCalc = statementEncase.substring(0, statementEncase.indexOf(" "));
			if (statementEncaseCalc.equals("GLOBAL") || statementEncaseCalc.equals("TELE") || statementEncaseCalc.equals("COORDS")) {
				// removes keyword
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1, statementEncase.length());
			}
		}

		statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1, statementEncase.length());

		return getLine.length() - statementEncase.length();
	}

	public static String[] parseDefinition(String getString, String getBegDef, int parseType, int getIndex, String fullLineGet) {
		/* parseType - 1 == def
		 * parseType - 2 == array
		 * parseType - 3 == 2d array
		 */

		String getBegString = getBegDef + "";
		String midStringSave = "";
		String getParamsString = "";
		String getEndString = "";

		String definitionCalc = "";

		// 0 - beg
		// 1 - mid - parsed definition
		// 2 - end
		// 3 - midStringSave - test for recurring definition
		String[] returnString = new String[4];

		Integer begIndexCalc = null;
		Integer endIndexCalc = null;

		if (parseType == 1) {

			// splits on definition name
			begIndexCalc = getString.indexOf(Var_Define.arrayDefineSave.get(getIndex)[2]);
			endIndexCalc = getString.indexOf(Var_Define.arrayDefineSave.get(getIndex)[2])
					+ Var_Define.arrayDefineSave.get(getIndex)[2].length();
		}

		if (parseType == 2) {

			// splits on array name
			begIndexCalc = getString.indexOf(Var_Array.singleArrayNameSave.get(getIndex)[2] + "[");
			endIndexCalc = getString.indexOf(Var_Array.singleArrayNameSave.get(getIndex)[2] + "[")
					+ Var_Array.singleArrayNameSave.get(getIndex)[2].length();
		}

		if (parseType == 3) {

			// splits on array name
			begIndexCalc = getString.indexOf(Var_Array.doubleArrayNameSave.get(getIndex)[2] + "[");
			endIndexCalc = getString.indexOf(Var_Array.doubleArrayNameSave.get(getIndex)[2] + "[")
					+ Var_Array.doubleArrayNameSave.get(getIndex)[2].length();
		}

		// gets everything before the definition
		getBegString += getString.substring(0, begIndexCalc);

		// gets the definition
		midStringSave = getString.substring(begIndexCalc, endIndexCalc);

		// gets parameters and anything after the definition
		getEndString = getString.substring(endIndexCalc);

		// checks if there are parameters in the first place (DEF ONLY)
		if (parseType == 1) {
			if (Integer.parseInt(Var_Define.arrayDefineSave.get(getIndex)[4]) > 0) {

				ArrayList<String> useParamsCalc = new ArrayList<String>();

				// if there is stuff past the definition and has () in the correct order
				if (getEndString.isEmpty() == false && getEndString.startsWith("(") && getEndString.contains(")")
						&& getEndString.indexOf("(") < getEndString.indexOf(")")) {

					// split params
					getParamsString = getEndString.substring(getEndString.indexOf("("), getEndString.indexOf(")") + 1);
					getEndString = getEndString.substring(getEndString.indexOf(")") + 1);
				}

				useParamsCalc = ParamUtils.getParams(getParamsString, Integer.parseInt(Var_Define.arrayDefineSave.get(getIndex)[4]));

				// replace all params
				definitionCalc = ParamUtils.replaceParams(Var_Define.arrayDefineSave.get(getIndex)[3], useParamsCalc,
						Integer.parseInt(Var_Define.arrayDefineSave.get(getIndex)[4]));

			} else {

				// no params
				definitionCalc = Var_Define.arrayDefineSave.get(getIndex)[3];

			}
		}

		// Gets specific definition from singleArray
		// Arr_Name[Index]
		// Arr_Name[-1]
		// Arr_Name[L]
		// Arr_Name[S]
		if (parseType == 2) {
			String calcIndexString = null;

			calcIndexString = getEndString.substring(getEndString.indexOf("[") + 1, getEndString.indexOf("]"));
			getEndString = getEndString.substring(getEndString.indexOf("]") + 1);

			if (NumberUtils.isNum(calcIndexString) == false) {
				calcIndexString = MathParser.parseSecondaryStatements(calcIndexString, fullLineGet);
				calcIndexString = MathParser.getOperation(calcIndexString, fullLineGet, false, 0);
			}

			if (NumberUtils.isNum(calcIndexString)) { // regular
				int indexCalc = Integer.parseInt(calcIndexString);

				// if it's -1, returns length - 1
				if (indexCalc == -1) {
					definitionCalc = (Var_Array.singleArraySave.get(getIndex).length - 1) + "";
				} else {

					// checks whether it's within the index
					if (Var_Array.singleArraySave.get(getIndex).length - 1 < indexCalc) {
						System.out.println("ERROR: Index '" + calcIndexString + "' in line '" + fullLineGet + "' is invalid");
						System.exit(0);
					}

					definitionCalc = Var_Array.singleArraySave.get(getIndex)[indexCalc] + "";
					midStringSave += "[" + calcIndexString + "]";
				}

			} else { // if 'S' or 'L'
				if (calcIndexString.equalsIgnoreCase("S")) { // element1;element2;element3
					String tempString = null;

					for (int i = 0; i < Var_Array.singleArraySave.get(getIndex).length; i++)
						if (tempString == null) {
							tempString = Var_Array.singleArraySave.get(getIndex)[i];
						} else {
							tempString += ";" + Var_Array.singleArraySave.get(getIndex)[i];
						}

					definitionCalc = tempString + "";
					midStringSave += "[" + calcIndexString + "]";

				} else {
					if (calcIndexString.equalsIgnoreCase("L")) {
						definitionCalc = (Var_Array.singleArraySave.get(getIndex).length) + "";

					} else {
						System.out.println("ERROR: Parameters '" + calcIndexString + "' in line '" + fullLineGet + "' are invalid");
						System.exit(0);
					}
				}
			}
		}

		// Gets specific definition from doubleArray
		/* Arr_Name[1][1]
		 * Arr_Name[1][S]
		 * Arr_Name[1][L]
		 * Arr_Name[1][-1]
		 * Arr_Name[L][L]
		 * Arr_Name[L]
		 * Arr_Name[-1]
		 */
		if (parseType == 3) {
			String calcIndexString = "";
			String calcIndexString2 = "";
			boolean parseArray = false;

			calcIndexString = getEndString.substring(getEndString.indexOf("[") + 1, getEndString.indexOf("]"));
			getEndString = getEndString.substring(getEndString.indexOf("]") + 1);

			if (getEndString.startsWith("[") && getEndString.contains("]")) { // gets calcIndexString2
				calcIndexString2 = getEndString.substring(getEndString.indexOf("[") + 1, getEndString.indexOf("]"));
				getEndString = getEndString.substring(getEndString.indexOf("]") + 1);

			} else {
				if (NumberUtils.isNum(calcIndexString) && calcIndexString.equals("-1") == false) {
					System.out.println(
							"ERROR: Array call '" + getString + "[" + calcIndexString + "]" + "' in '" + fullLineGet + "' is invalid");
					System.exit(0);
				}
			}

			if (NumberUtils.isNum(calcIndexString) == false) {
				calcIndexString = MathParser.parseSecondaryStatements(calcIndexString, fullLineGet);
				calcIndexString = MathParser.getOperation(calcIndexString, fullLineGet, false, 0);
			}

			if (NumberUtils.isNum(calcIndexString2) == false) {
				calcIndexString2 = MathParser.parseSecondaryStatements(calcIndexString2, fullLineGet);
				calcIndexString2 = MathParser.getOperation(calcIndexString2, fullLineGet, false, 0);
			}

			if (NumberUtils.isNum(calcIndexString)) {

				// checks index
				if (Var_Array.doubleArraySave.get(getIndex).length - 1 < Integer.parseInt(calcIndexString)
						&& Integer.parseInt(calcIndexString) != -1) {
					System.out.println("ERROR: Index '" + calcIndexString + "' in line '" + fullLineGet + "' is invalid");
					System.exit(0);
				}

				int indexCalc = Integer.parseInt(calcIndexString);

				if (indexCalc == -1) { // Arr_Name[-1]
					if (calcIndexString2.isEmpty()) {
						definitionCalc = (Var_Array.doubleArraySave.get(getIndex).length - 1) + "";
						parseArray = true;
					}
				}

				if (calcIndexString2.equals("-1")) { // Arr_Name[1][-1]
					definitionCalc = (Var_Array.doubleArraySave.get(getIndex)[indexCalc].length - 1) + "";
					parseArray = true;
				}

				if (NumberUtils.isNum(calcIndexString2) && calcIndexString2.equals("-1") == false) { // Arr_Name[1][1]

					// checks index
					if (Var_Array.doubleArraySave.get(getIndex)[indexCalc].length - 1 < Integer.parseInt(calcIndexString2)) {
						System.out.println("ERROR: Index '" + calcIndexString2 + "' in line '" + fullLineGet + "' is invalid");
						System.exit(0);
					}

					int indexCalc2 = Integer.parseInt(calcIndexString2);

					definitionCalc = (Var_Array.doubleArraySave.get(getIndex)[indexCalc][indexCalc2]) + "";
					midStringSave += "[" + calcIndexString + "][" + calcIndexString2 + "]";
					parseArray = true;
				}

				if (calcIndexString2.equalsIgnoreCase("L")) { // Arr_Name[1][L]
					definitionCalc = (Var_Array.doubleArraySave.get(getIndex)[indexCalc].length) + "";
					parseArray = true;
				}

				if (calcIndexString2.equalsIgnoreCase("S")) { // Arr_Name[1][S]
					String tempString = null;

					for (int i = 0; i < Var_Array.doubleArraySave.get(getIndex)[indexCalc].length; i++)
						if (tempString == null) {
							tempString = Var_Array.doubleArraySave.get(getIndex)[indexCalc][i];
						} else {
							tempString += ";" + Var_Array.doubleArraySave.get(getIndex)[indexCalc][i];
						}

					definitionCalc = tempString + "";
					midStringSave += "[" + calcIndexString + "][" + calcIndexString2 + "]";
					parseArray = true;
				}
			}

			if (calcIndexString.equalsIgnoreCase("L")) {
				if (calcIndexString2.isEmpty()) { // Arr_Name[L]
					definitionCalc = (Var_Array.doubleArraySave.get(getIndex).length) + "";
					parseArray = true;
				}

				if (calcIndexString2.equalsIgnoreCase("L")) { // Arr_Name[L][L] - why the hell would you use this
					int calcLength = 0;

					for (int i = 0; i < Var_Array.doubleArraySave.get(getIndex).length; i++) {
						calcLength += Var_Array.doubleArraySave.get(getIndex)[i].length;
					}

					definitionCalc = calcLength + "";
					parseArray = true;
				}
			}

			if (parseArray == false) { // fail lol
				System.out.println("ERROR: Array call '" + getString + "' in line '" + fullLineGet + "' is invalid");
				System.exit(0);
			}
		}

		int defType = 0;

		if (parseType == 1) {
			defType = Integer.parseInt(Var_Define.arrayDefineSave.get(getIndex)[0]);
		}

		if (parseType == 2) {
			defType = Integer.parseInt(Var_Array.singleArrayNameSave.get(getIndex)[0]);
		}

		if (parseType == 3) {
			defType = Integer.parseInt(Var_Array.doubleArrayNameSave.get(getIndex)[0]);
		}

		// checks whether it is a TELE or COORDS definition with [ and ]
		if (defType == 4 || defType == 5) {

			// string array to get 2 strings
			// they have to be seperate because recurring definition tests are done using defintionCalc
			String[] getStringArray = null;

			getStringArray = ParamUtils.parseCoordinates(getEndString, definitionCalc, defType, fullLineGet);

			definitionCalc = getStringArray[0];
			getEndString = getStringArray[1];
		}

		returnString[0] = getBegString;
		returnString[1] = definitionCalc;
		returnString[2] = getEndString;
		returnString[3] = midStringSave;

		// System.out.println(getBegString + " | " + definitionCalc + " | " + getEndString + " | " + midStringSave);

		return returnString;
	}
}
