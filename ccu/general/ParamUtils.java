package ccu.general;

import java.util.ArrayList;
import java.util.regex.Pattern;

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
	public static ArrayList<String> replaceParams(ArrayList<String> getArray, ArrayList<String> getParams, int paramNum) {
		String lineCalc = null;
		ArrayList<String> returnArray = new ArrayList<String>();

		for (int funcIndex = 0; funcIndex < getArray.size(); funcIndex++) {
			if (paramNum > 0) {
				lineCalc = getArray.get(funcIndex);
				for (int paramIndex = 0; paramIndex < paramNum; paramIndex++) {
					lineCalc = lineCalc.replace(("|" + paramIndex + "|"), getParams.get(paramIndex));
				}
				returnArray.add(lineCalc);
			}
		}

		return returnArray;
	}

	// Calc all future params in a string (aka |1;2| --> |1;1| and |1;1| --> |1|)
	public static String calcFutureParams(String getString) {

		boolean changedLine = false;
		String lineCalc = null;

		if (getString.contains("|")) {
			String[] paramsCalc = getString.split(Pattern.quote("|"));
			String[] paramsCalc2 = null;
			int paramIntCalc = 0;
			int paramIndex = 0;

			while (paramIndex < paramsCalc.length) {
				// if it has ; and there is only one ;
				if (paramsCalc[paramIndex].contains(";")
						&& paramsCalc[paramIndex].length() - paramsCalc[paramIndex].replace(";", "").length() == 1) {
					paramsCalc2 = paramsCalc[paramIndex].split(";");

					// if both are integers
					if (NumberUtils.isInt(paramsCalc2[0]) && NumberUtils.isInt(paramsCalc2[1])) {
						paramIntCalc = Integer.parseInt(paramsCalc2[1]) - 1;
						if (paramIntCalc == 0) {
							paramsCalc[paramIndex] = paramsCalc2[0];
						} else {
							paramsCalc[paramIndex] = paramsCalc2[0] + ";" + paramIntCalc;
						}

						changedLine = true;
					}

					if (paramsCalc.length - 1 == paramIndex) {
						paramsCalc[paramIndex] += "|";
					}

					paramIndex += 2;
					continue;
				}
				paramIndex++;
			}

			if (changedLine == true) {
				for (int i = 0; i < paramsCalc.length; i++) {
					if (i == 0) {
						lineCalc = paramsCalc[0];
					} else {
						lineCalc += "|" + paramsCalc[i];
					}
				}
			} else {
				lineCalc = getString;
			}
		} else {
			lineCalc = getString;
		}

		return lineCalc;
	}

	// Calc all future params in a string (aka |1;2| --> |1;1| and |1;1| --> |1|)
	public static ArrayList<String> calcFutureParams(ArrayList<String> getArray) {

		boolean changedLine = false;
		String lineCalc = null;

		for (int arrayIndex = 0; arrayIndex < getArray.size(); arrayIndex++) {

			if (getArray.get(arrayIndex).contains("|")) {
				String[] paramsCalc = getArray.get(arrayIndex).split(Pattern.quote("|"));
				String[] paramsCalc2 = null;
				int paramIntCalc = 0;
				int paramIndex = 0;

				while (paramIndex < paramsCalc.length) {
					// if it has ; and there is only one ;
					if (paramsCalc[paramIndex].contains(";")
							&& paramsCalc[paramIndex].length() - paramsCalc[paramIndex].replace(";", "").length() == 1) {
						paramsCalc2 = paramsCalc[paramIndex].split(";");

						// if both are integers
						if (NumberUtils.isInt(paramsCalc2[0]) && NumberUtils.isInt(paramsCalc2[1])) {
							paramIntCalc = Integer.parseInt(paramsCalc2[1]) - 1;
							if (paramIntCalc == 0) {
								paramsCalc[paramIndex] = paramsCalc2[0];
							} else {
								paramsCalc[paramIndex] = paramsCalc2[0] + ";" + paramIntCalc;
							}

							changedLine = true;
						}

						if (paramsCalc.length - 1 == paramIndex) {
							paramsCalc[paramIndex] += "|";
						}

						paramIndex += 2;
						continue;
					}
					paramIndex++;
				}

				if (changedLine == true) {
					for (int i = 0; i < paramsCalc.length; i++) {
						if (i == 0) {
							lineCalc = paramsCalc[0];
						} else {
							lineCalc += "|" + paramsCalc[i];
						}
					}
					getArray.set(arrayIndex, lineCalc);
				}
			}
		}

		return getArray;
	}
}
