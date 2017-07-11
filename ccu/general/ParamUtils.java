package ccu.general;

import java.util.ArrayList;
import java.util.regex.Pattern;

/* TODO
 * Parameters should be thought of --
 * 	whenever a tab space occurs because of LOOP / FUNC / DEF
 * 		-increases 2nd number by 1, and starts replacing
 *	parameters are replaced before checkCommands
 */

public class ParamUtils {
	// count number of params in a string
	public static int countParams(String getParamString) {
		Integer paramMaxNum = null;

		if (getParamString.trim().contains("|")) {
			String[] paramsCalc = getParamString.trim().split(Pattern.quote("|"));
			int paramIndex = 0;

			while (paramIndex < paramsCalc.length) {
				if (NumberUtils.isInt(paramsCalc[paramIndex])) {
					if (paramMaxNum == null || paramMaxNum < Integer.parseInt(paramsCalc[paramIndex])) {
						paramMaxNum = Integer.parseInt(paramsCalc[paramIndex]);
					}
					paramIndex += 2;
					continue;
				}
				paramIndex++;
			}
		}

		if (paramMaxNum == null) {
			return 0;
		} else {
			return paramMaxNum + 1;
		}
	}

	// count number of params in an array list
	public static int countParams(ArrayList<String> getParamsArray) {
		Integer paramMaxNum = null;

		for (int i = 0; i < getParamsArray.size(); i++) {
			if (getParamsArray.get(i).trim().contains("|")) {
				String[] paramsCalc = getParamsArray.get(i).trim().split(Pattern.quote("|"));
				int paramIndex = 0;

				while (paramIndex < paramsCalc.length) {
					if (NumberUtils.isInt(paramsCalc[paramIndex])) {
						if (paramMaxNum == null || paramMaxNum < Integer.parseInt(paramsCalc[paramIndex])) {
							paramMaxNum = Integer.parseInt(paramsCalc[paramIndex]);
						}
						paramIndex += 2;
						continue;
					}
					paramIndex++;
				}
			}
		}

		if (paramMaxNum == null) {
			return 0;
		} else {
			return paramMaxNum + 1;
		}
	}

	// gets all params within round brackets
	// getParams includes round brackets
	public static ArrayList<String> getParams(String getParams, int paramNum) {

		ArrayList<String> useParamsCalc = new ArrayList<String>();
		String[] getParamsCalc = null;

		if (paramNum > 0) {
			// gets params

			// if it's empty or has no bracketss
			if (getParams == null || getParams.isEmpty() || getParams.substring(1, getParams.length() - 1).isEmpty()) {
				for (int i = 0; i < paramNum; i++) {
					useParamsCalc.add("");
				}
			} else {

				// add all existing parameters, even if there's more than enough
				getParamsCalc = getParams.substring(1, getParams.length() - 1).split(";");
				for (int i = 0; i < getParamsCalc.length; i++) {
					useParamsCalc.add(getParamsCalc[i]);
				}

				// check if there are more params to be added
				if (getParamsCalc.length < paramNum) {
					for (int i = getParamsCalc.length; i < paramNum; i++) {
						useParamsCalc.add("");
					}
				}
			}
			return useParamsCalc;
		} else {

			// returns null if there are no params
			return null;
		}
	}

	// Get loop params from an ArrayList<String[]>
	public static ArrayList<String> getLoopParams(ArrayList<String[]> getLoopArray, int loopIndex, int paramNum) {
		ArrayList<String> returnArray = new ArrayList<String>();

		for (int i = 0; i < paramNum; i++) {
			if (getLoopArray.size() - 1 < i) {
				returnArray.add("");
			} else {
				if (getLoopArray.get(i).length > loopIndex) {
					returnArray.add(getLoopArray.get(i)[loopIndex]);
				} else {
					returnArray.add("");
				}
			}
		}

		return returnArray;
	}

	// Replaces all parameters in a string
	public static String replaceParams(String getString, ArrayList<String> getParams, int paramNum) {
		
		if (paramNum > 0) {
			for (int paramIndex = 0; paramIndex < paramNum; paramIndex++) {
				getString = getString.replace(("|" + paramIndex + "|"), getParams.get(paramIndex));
			}
		}
		
		return getString;
	}

	// Replaces all parameters in an array
	public static ArrayList<String> replaceParams(ArrayList<String> getArray, ArrayList<String> getParams, int paramNum, int tabNum) {
		
		String lineCalc = null;
		ArrayList<String> returnArray = new ArrayList<String>();
		
		// if there's no params in the first place
		if (getParams == null || getParams.isEmpty()) {
			return getArray;
		}

		// calcs number of tab spaces
		int tabNumCalc = 0;

		// saves previous number of tab spaces
		int tabNumPrevious = 0;

		// calcs number of param encapsulations
		int paramEncapsulate = 0;

		// Current state of param encapsulations
		int paramEncapsulateGet = 0;

		// for each tab space, stores param encapsulation number
		ArrayList<Integer> paramEncapsulateArray = new ArrayList<Integer>();

		paramEncapsulateArray.add(0);
		tabNumCalc = tabNum + 0;

		for (int funcIndex = 0; funcIndex < getArray.size(); funcIndex++) {

			// if there's more than one param
			if (paramNum > 0) {

				lineCalc = getArray.get(funcIndex);

				// gets tab number
				tabNumPrevious = tabNumCalc + 0;
				tabNumCalc = StringUtils.countChars(lineCalc, "\t");

				// meaning tabnum went up - check if previous was FUNC or LOOP
				if (tabNumCalc > tabNumPrevious) {
					if (funcIndex > 0 && (getArray.get(funcIndex - 1).trim().startsWith("FUNC")
							|| getArray.get(funcIndex - 1).trim().startsWith("LOOP"))) {

						// if success, adds paramEncapsulateArray with paramEncapsulate++
						paramEncapsulate++;
					}
					paramEncapsulateArray.add(paramEncapsulate);
				}

				// meaning it went down
				if (tabNumCalc < tabNumPrevious) {

					// checks if it's an invalid amount missing for some reason
					if (tabNumCalc < tabNum) {
						System.out.println(
								"ERROR: Tab spaces are off when replacing parameters starting from line '" + getArray.get(0) + "'");
						System.exit(0);
					}

					// removes previous number of however many there were
					for (int i = 0; i < (tabNumPrevious - tabNumCalc); i++) {
						paramEncapsulateArray.remove(paramEncapsulateArray.size() - 1);
					}
				}
				
				// check if it's a definition - temp increases paramEncapsulate
				if (lineCalc.trim().startsWith("DEF")) {
					paramEncapsulateArray.set(paramEncapsulateArray.size() - 1, paramEncapsulate + 1);
				}
				
				// only if paramEncapsulate is 0
				paramEncapsulateGet = paramEncapsulateArray.get(tabNumCalc - tabNum);
				
				if (paramEncapsulateGet == 0) {
					for (int paramIndex = 0; paramIndex < paramNum; paramIndex++) {
						lineCalc = lineCalc.replace(("|" + paramIndex + "|"), getParams.get(paramIndex));
					}
				} else {
					for (int paramIndex = 0; paramIndex < paramNum; paramIndex++) {
						lineCalc = lineCalc.replace(("|" + paramIndex + ";" + paramEncapsulateGet + "|"), getParams.get(paramIndex));
					}
				}
				
				// check if it's a definition - undos temp increase in paramEncapsulate 
				if (lineCalc.trim().startsWith("DEF")) {
					paramEncapsulateArray.set(paramEncapsulateArray.size() - 1, paramEncapsulate - 1);
				}

				returnArray.add(lineCalc);
			}
		}
		
		// System.out.println(getArray);
		// System.out.println("");
		
		return returnArray;
		
		
	}
}
