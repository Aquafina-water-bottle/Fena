package ccu.general;

import java.text.DecimalFormat;
import java.util.ArrayList;

public class NumberUtils {
	
	// get max number
	public static int getMaxSize(ArrayList<String[]> arrayGet) {
		int numCalc = 0;
		
		if (arrayGet.isEmpty()) {
			return 0;
		}
		
		if (arrayGet.size() == 1) {
			return arrayGet.get(0).length;
		}
		
		for (int i = 0; i < arrayGet.size(); i++) {
			if (arrayGet.get(i).length > numCalc) {
				numCalc = arrayGet.get(i).length;
			}
		}
		
		return numCalc;
	}
	
	// checks if it's a number (int or float)
	public static boolean isNum(String testNum) {
		if (testNum == null) {
			return false;
		}
		try {
			Integer.parseInt(testNum);
			return true;
		} catch (NumberFormatException e) {
			try {
				Float.parseFloat(testNum);
				return true;
			} catch (NumberFormatException e2) {
				return false;
			}
		}
	}

	// checks if it's an int and only an int
	public static boolean isInt(String testInt) {
		if (testInt == null) {
			return false;
		} else {
			try {
				Integer.parseInt(testInt);
				return true;
			} catch (NumberFormatException e) {
				return false;
			}
		}
	}

	// checks if it's a float and only a float
	public static boolean isFloat(String testFloat) {
		if (testFloat == null) {
			return false;
		} else {
			try {
				// if it's a float
				Float.parseFloat(testFloat);
				try {

					// cannot be a float if it works as an int
					Integer.parseInt(testFloat);
					return false;

				} catch (NumberFormatException e) {
					return true;
				}
			} catch (NumberFormatException e) {
				return false;
			}
		}
	}

	public static String roundFloat(float getFloat) {
		String roundCalc = new DecimalFormat("#.#####").format(getFloat);
		if (roundCalc.contains(".") == false) {
			roundCalc += ".0";
		}
		return roundCalc;
	}

	public static boolean checkSameSign(float x, float y) {
		if ((x >= 0 && y >= 0) || (x < 0 && y < 0)) {
			return true;
		} else {
			return false;
		}
	}

	public static boolean checkSameSign(int x, int y) {
		if ((x >= 0 && y >= 0) || (x < 0 && y < 0)) {
			return true;
		} else {
			return false;
		}
	}
}
