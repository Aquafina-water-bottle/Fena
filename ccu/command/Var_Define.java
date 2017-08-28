package ccu.command;

import java.util.ArrayList;

import ccu.general.ArgUtils;
import ccu.general.NumberUtils;
import ccu.general.ParamUtils;
import ccu.general.StringUtils;

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
			"DEF", "ARRAY", "SET", "SPLIT", "MAX", "GLOBAL", "TEMP", "RETURN", "COORDS", "TELE", 
			"GROUP", "PULSE", "CLOCK", "BLOCK",
			"USE", "BEG", "END", "NOSPACE",
			"FUNC", "ACTIVATE", "PARSESEP", "CALL", 
			"MFUNC", "BRANCH",
			"IMPORT", "LIBRARY", "GETDIR", "WITHIN", "GETCOORDS", 
			"CALC", "SIN", "COS", "TAN", "ABS", "LOG", "LOG10", "INT", "DOUBLE",
			"GSELF", "ISIMPORT",
			"COND", "OPTIONS", "IF", "ELSE", "ELIF", "LOOP", "INITIALIZE", "FINALIZE", 
			"PRINT", "EXIT", "UNASSIGN"
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

		String[] arrayDefineCalc = new String[6];
		Integer defineType = null;
		Integer visibilityType = null; // 1 = global, 2 = temp

		String defineName = null;
		String defintionGet = null;
		Integer splitNum = null;
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
		if (statementEncase.contains(" ")) {
			switch (statementEncase.substring(0, statementEncase.indexOf(" "))) {
			case "GLOBAL":
				visibilityType = 1;
				// removes GLOBAL
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1);
				break;
				
			case "TEMP":
				visibilityType = 2;
				// removes TEMP
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1);
				break;
				
			case "RETURN":
				visibilityType = 3;
				// removes TEMP
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
				
			case "MAX":
				// removes MAX
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1);

				if (statementEncase.contains(" ") == false) {
					System.out.println("ERROR: Invalid arguments for 'MAX' in line '" + this.fullLineGet + "'");
					System.exit(0);
				}

				String splitNumTest = statementEncase.substring(0, statementEncase.indexOf(" "));
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1);
				if (NumberUtils.isInt(splitNumTest)) {
					splitNum = Integer.parseInt(splitNumTest);
				} else {
					System.out.println("ERROR: 'MAX' in line '" + this.fullLineGet + "' must be proceeded with an integer");
					System.exit(0);
				}
				break;
			}
		}
		
		// Gets second parameters
		if (statementEncase.contains(" ")) {
			switch (statementEncase.substring(0, statementEncase.indexOf(" "))) {
			case "GLOBAL":
				if (visibilityType == null) {
					visibilityType = 1;
				} else {
					System.out.println(
							"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
				// removes GLOBAL
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1, statementEncase.length());
				break;
				
			case "TEMP":
				if (visibilityType == null) {
					visibilityType = 2;
				} else {
					System.out.println(
							"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
				// removes GLOBAL
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1, statementEncase.length());
				break;
				
			case "RETURN":
				if (visibilityType == null) {
					visibilityType = 3;
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
				
			case "MAX":
				// removes MAX
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1);
				
				if (statementEncase.contains(" ") == false) {
					System.out.println("ERROR: Invalid arguments for 'MAX' in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
				
				if (splitNum == null) {
					String splitNumTest = statementEncase.substring(0, statementEncase.indexOf(" "));
					statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1);
					if (NumberUtils.isInt(splitNumTest)) {
						splitNum = Integer.parseInt(splitNumTest);
					} else {
						System.out.println("ERROR: 'MAX' in line '" + this.fullLineGet + "' must be proceeded with an integer");
						System.exit(0);
					}
				} else {
					System.out.println(
							"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
				break;
			}
		}
		
		// Gets third parameters
		if (statementEncase.contains(" ")) {
			switch (statementEncase.substring(0, statementEncase.indexOf(" "))) {
			case "GLOBAL":
				if (visibilityType == null) {
					visibilityType = 1;
				} else {
					System.out.println(
							"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
				// removes GLOBAL
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1, statementEncase.length());
				break;
				
			case "TEMP":
				if (visibilityType == null) {
					visibilityType = 2;
				} else {
					System.out.println(
							"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
				// removes GLOBAL
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1, statementEncase.length());
				break;
				
			case "RETURN":
				if (visibilityType == null) {
					visibilityType = 3;
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

			case "MAX":
				// removes MAX
				statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1);

				if (statementEncase.contains(" ") == false) {
					System.out.println("ERROR: Invalid arguments for 'MAX' in line '" + this.fullLineGet + "'");
					System.exit(0);
				}

				if (splitNum == null) {
					String splitNumTest = statementEncase.substring(0, statementEncase.indexOf(" "));
					statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1);
					if (NumberUtils.isInt(splitNumTest)) {
						splitNum = Integer.parseInt(splitNumTest);
					} else {
						System.out.println("ERROR: 'MAX' in line '" + this.fullLineGet + "' must be proceeded with an integer");
						System.exit(0);
					}
				} else {
					System.out.println(
							"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
				break;
			}
			// the end should make 'statementEncase' as the actual use thing (Name Definition)
		}
		
		// Sets name
		if (statementEncase.contains(" ")) {
			defineName = statementEncase.substring(0, statementEncase.indexOf(" ")).replace("`", "");
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
			if (statementEncase.isEmpty()) {
				System.out.println("ERROR: '" + this.fullLineGet + "' does not define anything");
				System.exit(0);
			} else {
				defineName = statementEncase.replace("`", "");
				defintionGet = "";
			}
		}

		// sets options if they are unspecified
		if (visibilityType == null) {
			visibilityType = 0;
		}
		// detects definition type if not specified

		// Sets to string
		if (defineType == null) {
			defineType = 1;
		}

		// tests whether coords works
		ArgUtils.checkCoords(defintionGet, defineType, this.fullLineGet);
		
		// if splitNum is null
		if (splitNum == null) {
			splitNum = -1;
		}
		
		// If global, tabnum = 0
		switch (visibilityType) {
		case 1:
			this.tabNum = 0;
			break;
			
		case 2:
			this.tabNum += 1;
			break;
			
		case 3:
			this.tabNum -= 1;
			break;
		}

		arrayDefineCalc[0] = defineType.toString();
		arrayDefineCalc[1] = tabNum + "";
		arrayDefineCalc[2] = defineName;
		arrayDefineCalc[3] = defintionGet;
		arrayDefineCalc[4] = paramMaxNum + "";
		arrayDefineCalc[5] = splitNum + "";

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

		if (statementEncase.contains(" ")) {
			statementEncase = statementEncase.substring(statementEncase.indexOf(" ") + 1, statementEncase.length());
			return getLine.length() - statementEncase.length();
		} else {
			return getLine.length();
		}

	}

	public static String[] parseDefinition(String getString, String getBegDef, int parseType, int getIndex, int tabNum,
			String fullLineGet) {
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
					String[] getInside = StringUtils.getInside(getEndString, "", "(", ")", true);
					getParamsString = getInside[1];
					getEndString = getInside[2];
					
					/*
					getParamsString = getEndString.substring(getEndString.indexOf("("), getEndString.indexOf(")") + 1);
					getEndString = getEndString.substring(getEndString.indexOf(")") + 1);
					*/
				}

				// check for definitions within the parameters
				getParamsString = Var_Define.calcDefine(getParamsString, tabNum, fullLineGet);
				useParamsCalc = ParamUtils.getParams(getParamsString, Integer.parseInt(Var_Define.arrayDefineSave.get(getIndex)[4]), Integer.parseInt(Var_Define.arrayDefineSave.get(getIndex)[5]));

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

			String[] getInsideCalc = StringUtils.getInside(getEndString, "", "[", "]", true);
			calcIndexString = getInsideCalc[3];
			getEndString = getInsideCalc[2];
			
			calcIndexString = Var_Define.calcDefine(calcIndexString, tabNum, fullLineGet);

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
						System.out.println("ERROR: Index '" + Var_Array.singleArrayNameSave.get(getIndex)[2] + "' in line '"
								+ fullLineGet + "' is invalid");
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

			String[] getInsideCalc = StringUtils.getInside(getEndString, "", "[", "]", true);
			calcIndexString = getInsideCalc[3];
			calcIndexString = Var_Define.calcDefine(calcIndexString, tabNum, fullLineGet);
			getEndString = getInsideCalc[2];

			if (getEndString.startsWith("[") && getEndString.contains("]")) { // gets calcIndexString2
				getInsideCalc = StringUtils.getInside(getEndString, "", "[", "]", true);
				calcIndexString2 = getInsideCalc[3];
				calcIndexString2 = Var_Define.calcDefine(calcIndexString2, tabNum, fullLineGet);
				getEndString = getInsideCalc[2];

			} else {
				if (NumberUtils.isNum(calcIndexString) && calcIndexString.equals("-1") == false) {
					System.out.println("ERROR: Array call '" + Var_Array.doubleArrayNameSave.get(getIndex)[2] + "[" + calcIndexString
							+ "]" + "' in '" + fullLineGet + "' is invalid");
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
				System.out.println("ERROR: Array call '" + calcIndexString2 + "' in line '" + fullLineGet + "' is invalid");
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

	public static String calcDefine(String getString, int tabNum, String fullLineGet) {
		// Gets beginning 'DEF' part if it exists, and just gets the whole line if it doesn't
		String giveDefString = "";
		String getBegDef = "";
		String[] getDefinitionArray = null;
		boolean recheckLine = false;
		String definitionCalc = null;
		ArrayList<String> usedDefinitionArray = new ArrayList<String>();

		do {
			definitionCalc = null;
			getBegDef = "";
			giveDefString = "";

			recheckLine = false;
			getDefinitionArray = null;

			// undergoes PARSE()
			String[] parseArray = null;
			parseArray = StringUtils.parseInside(getString);
			if (parseArray != null) {
				getString = parseArray[0] + parseArray[1] + parseArray[2];
			}
			
			// when the line starts with 'DEF'
			if (getString.trim().length() >= 3 && getString.trim().substring(0, 3).equals("DEF") == true) {
				giveDefString = getString.substring(Var_Define.getDefineIndex(getString));
				getBegDef = getString.substring(0, Var_Define.getDefineIndex(getString));
			} else {
				giveDefString = getString;
			}

			// iterates through all definitions
			// starts at the negative end to prioritize the more tabulated definition
			for (int defIndex = Var_Define.arrayDefineSave.size() - 1; defIndex >= 0; defIndex--) {

				// if a definition matches up (cannot be with UNASSIGN)
				if (giveDefString.trim().contains(Var_Define.arrayDefineSave.get(defIndex)[2])
						&& tabNum >= Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[1])
						&& giveDefString.trim().startsWith("UNASSIGN") == false) {
					recheckLine = true;

					getDefinitionArray = Var_Define.parseDefinition(giveDefString, getBegDef, 1, defIndex, tabNum, getString);
					definitionCalc = getDefinitionArray[1] + "";
					break;
				}
			}

			if (recheckLine == false) {
				getBegDef = "";
				giveDefString = "";

				// when the line starts with 'SET'
				if (getString.trim().length() >= 3 && getString.trim().substring(0, 3).equals("SET") == true) {
					giveDefString = getString.substring(Var_Array.getArrayIndex(getString));
					getBegDef = getString.substring(0, Var_Array.getArrayIndex(getString));
				} else {
					giveDefString = getString;
				}

				// iterates through all single arrays
				// starts at the negative end to prioritize the more tabulated array
				for (int arrayIndex = Var_Array.singleArrayNameSave.size() - 1; arrayIndex >= 0; arrayIndex--) {

					giveDefString = getString;

					// if an array matches up (cannot be with UNASSIGN or ARRAY)
					if (giveDefString.trim().contains(Var_Array.singleArrayNameSave.get(arrayIndex)[2] + "[")
							&& tabNum >= Integer.parseInt(Var_Array.singleArrayNameSave.get(arrayIndex)[1])
							&& giveDefString.trim().startsWith("UNASSIGN") == false && giveDefString.trim().startsWith("SET") == false
							&& giveDefString.trim().startsWith("ARRAY") == false) {
						recheckLine = true;

						getDefinitionArray = Var_Define.parseDefinition(giveDefString, getBegDef, 2, arrayIndex, tabNum, getString);
						definitionCalc = getDefinitionArray[1] + "";
					}
				}
			}

			if (recheckLine == false) {
				// iterates through all double arrays
				// starts at the negative end to prioritize the more tabulated array
				for (int arrayIndex = Var_Array.doubleArrayNameSave.size() - 1; arrayIndex >= 0; arrayIndex--) {
					giveDefString = getString;

					// if an array matches up (cannot be with UNASSIGN or ARRAY)
					if (giveDefString.trim().contains(Var_Array.doubleArrayNameSave.get(arrayIndex)[2] + "[")
							&& tabNum >= Integer.parseInt(Var_Array.doubleArrayNameSave.get(arrayIndex)[1])
							&& giveDefString.trim().startsWith("UNASSIGN") == false
							&& giveDefString.trim().startsWith("ARRAY") == false) {
						recheckLine = true;

						getDefinitionArray = Var_Define.parseDefinition(giveDefString, getBegDef, 3, arrayIndex, tabNum, getString);
						definitionCalc = getDefinitionArray[1] + "";
					}
				}
			}

			if (recheckLine) {
				
				// tests for recurring definition
				for (String testDefinition : usedDefinitionArray) {
					if (definitionCalc.contains(testDefinition)) {
						System.out.println("ERROR: Recurring definition at line '" + fullLineGet + "' starting with the definition '"
								+ testDefinition + "'");
						System.out.println(definitionCalc + " | " + testDefinition);
						System.exit(0);
					}
				}

				// sees if there is any definition inside definitionCalc - if not, clears usedDefinitionArray
				boolean foundDefinition = false;

				for (int defIndex = Var_Define.arrayDefineSave.size() - 1; defIndex >= 0; defIndex--) {
					if (definitionCalc.trim().contains(Var_Define.arrayDefineSave.get(defIndex)[2])) {
						foundDefinition = true;
						break;
					}
				}

				if (foundDefinition == false) {
					for (int arrayIndex = Var_Array.singleArrayNameSave.size() - 1; arrayIndex >= 0; arrayIndex--) {
						// if an array matches up (cannot be with UNASSIGN or ARRAY)
						if (definitionCalc.trim().contains(Var_Array.singleArrayNameSave.get(arrayIndex)[2] + "[")) {
							foundDefinition = true;
							break;
						}
					}
				}

				if (foundDefinition == false) {
					for (int arrayIndex = Var_Array.doubleArrayNameSave.size() - 1; arrayIndex >= 0; arrayIndex--) {
						if (definitionCalc.trim().contains(Var_Array.doubleArrayNameSave.get(arrayIndex)[2] + "[")) {
							foundDefinition = true;
							break;
						}
					}
				}

				if (foundDefinition == false) {
					// meaning it's useless to keep the usedDefinitionArra
					usedDefinitionArray.clear();
				} else {
					// adds to check for recurring definition
					usedDefinitionArray.add(getDefinitionArray[3]);
				}

				// properly sets the line
				getString = getDefinitionArray[0] + getDefinitionArray[1] + getDefinitionArray[2];
			}

		} while (recheckLine);
		

		// removes PARSE()
		getString = StringUtils.removeParse(getString);
		
		return getString;
	}
	
	public static void garbageCollect(int tabNum, int resetlastFunc) {
		boolean resetIndexCalc = false;
		
		// reset all definitions that don't work with the decreasing tab numbers
		for (int defIndex = 0; defIndex < arrayDefineSave.size(); defIndex++) {
			if ((resetlastFunc <= 1) && defIndex == arrayDefineSave.size() - 1) {
				break;
			}
			
			if (resetIndexCalc == true) {
				resetIndexCalc = false;
				defIndex = 0;
			}
			if (tabNum <= Integer.parseInt(arrayDefineSave.get(defIndex)[1])) {
				resetIndexCalc = true;
				arrayDefineSave.remove(defIndex);
			}
		}
	}
}
