package ccu.general;

public class NumberUtils {
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

	public static boolean isFloat(String testFloat) {
		if (testFloat == null) {
			return false;
		} else {
			try {
				Float.parseFloat(testFloat);
				return true;
			} catch (NumberFormatException e) {
				return false;
			}
		}
	}

	public static String roundFloat(float getFloat, int roundNum) {
		String roundCalc = "";
		String getNum = getFloat + "";
		if (getNum.substring(getNum.indexOf(".") + 1).length() > roundNum) {
			roundCalc = getNum.substring(0, getNum.indexOf(".") + roundNum + 1);
			if (Integer.parseInt(roundCalc.substring(roundCalc.indexOf(".") + 1)) == 0) {
				roundCalc = getNum.substring(0, getNum.indexOf(".") + 2);
			}
			return roundCalc;
		}

		String asdf = getNum.substring(getNum.indexOf(".") + 1);
		Float.parseFloat(asdf.trim());
		if (Integer.parseInt(getNum.substring(getNum.indexOf(".") + 1)) == 0) {
			getNum = getNum.substring(0, getNum.indexOf(".") + 2);
		}

		return getNum;
	}

	public static boolean checkSameSign(float x, float y) {
		if ((x >= 0 && y >= 0) || (x < 0 && y < 0)) {
			return true;
		} else {
			return false;
		}
	}
}
