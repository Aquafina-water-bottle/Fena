package ccu.general;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.regex.Pattern;

public class GeneralFile {
	private File fileName = null;
	public String fileString = null;

	// constructor if the file is a string
	public GeneralFile(String fileName) {
		this.fileName = new File(fileName);
		fileString = this.fileName.getName();
	}

	// constructor if the file is a File object
	public GeneralFile(File fileName) {
		this.fileName = fileName;
		fileString = this.fileName.getName();
	}

	// just general stuff really
	public static void dispError(Exception e) {
		System.out.println("UNKNOWN ERROR:");
		e.printStackTrace();
	}

	// gets file array
	public ArrayList<String> getFileArray() {
		InputStream in = null;

		// Reading a file errors
		try {
			in = new FileInputStream(this.fileName);
		} catch (FileNotFoundException e) {
			System.out.println("ERROR: Could not find the file: \n" + e);
			System.exit(0);
		} catch (Exception e) {
			System.out.println("UNKNOWN ERROR: Could not find the file: \n" + e);
			System.exit(0);
		}

		System.out.println("Successfully found the file: " + this.fileString);

		// tbh idk what this does
		BufferedReader reader = new BufferedReader(new InputStreamReader(in));
		ArrayList<String> doc = new ArrayList<String>();

		// removes all empty lines as well as pure whitespace lines
		// transfers all lines to doc
		String line;
		try {
			while ((line = reader.readLine()) != null) {
				if (line.trim().isEmpty() == false) {
					doc.add(line);
				}
			}
			reader.close();

		} catch (IOException e) {
			dispError(e);
		}
		return doc;
	}

	public static ArrayList<String> parseCCU(ArrayList<String> getArray) {
		ArrayList<String> returnArray =removeRightWhiteSpace(removeSkipLineBlock(
				combineLine(removeComment(removeCommentBlock(escapeLine(getArray, "`"), "//=", "=//"), "//", true), "\\"), "/*", "*/",
				"-/-"));
		return returnArray;
	}

	public static ArrayList<String> removeRightWhiteSpace(ArrayList<String> getArray) {
		ArrayList<String> returnArray = new ArrayList<String>();
		for (int i = 0; i < getArray.size(); i++) {
			returnArray.add(getArray.get(i).replaceAll("\\s+$", ""));
		}
		return returnArray;
	}

	public static ArrayList<String> combineLine(ArrayList<String> getArray, String getChar) {
		ArrayList<String> returnArray = new ArrayList<String>();
		String calcString = "";
		boolean combineLine = false;

		for (int i = 0; i < getArray.size(); i++) {

			combineLine = false;
			if (getArray.get(i).endsWith(getChar)) {
				combineLine = true;
			}

			if (combineLine == true) {
				if (calcString.isEmpty()) {
					calcString += getArray.get(i).substring(0, getArray.get(i).length() - 1);
				} else {

					// trims to get rid of any whitespace in the front of the string
					String testString = getArray.get(i).trim().substring(0, getArray.get(i).trim().length() - 1);
					if (testString.startsWith("CCU_COND_")) {
						testString = testString.substring(9);
					}
					calcString += testString;
				}

				// if the document ended
				if (i == getArray.size() - 1) {
					returnArray.add(calcString);
				}

			} else {
				if (calcString.isEmpty()) {
					returnArray.add(getArray.get(i));
				} else {
					String testString = getArray.get(i).trim().substring(0, getArray.get(i).trim().length());
					calcString += testString;
					returnArray.add(calcString);
					calcString = "";
				}
			}
		}
		return returnArray;
	}

	public static ArrayList<String> escapeLine(ArrayList<String> arrayGet, String escapeChar) {

		ArrayList<String> returnArray = new ArrayList<String>();

		for (String line : arrayGet) {
			StringBuilder sb = new StringBuilder();

			// adds this because it doesn't split properly if it ends with '`'
			line += " ";
			String[] splitEscape = line.split(Pattern.quote(escapeChar));

			for (int i = 0; i < splitEscape.length; i++) {
				if (i % 2 == 1) {
					String[] splitArray = splitEscape[i].split("|");
					for (String charInArray : splitArray) {
						sb.append(escapeChar + charInArray);
					}

					sb.append("`");
				} else {
					sb.append(splitEscape[i]);
				}
			}
			returnArray.add(sb.substring(0, sb.length() - 1).replace("``", ""));
		}

		return returnArray;
	}

	public static String checkFileExtension(String fileGet, String fileExtension, boolean createFile, boolean isStrict) {
		// isStrict means if the fileExtension is just '.ccu' (strict) or '_dat.txt' (not strict)
		// aka whether it's a "." at the beginning or not apparently idk why i made this

		if (isStrict) {
			if (fileGet.contains(".")) {
				if (fileGet.substring(fileGet.lastIndexOf(".")).equals(fileExtension)) {
					// success
					// System.out.println("File created: '" + fileGet + "'");
				} else {
					if (createFile) {
						String fileTypeTemp = fileGet.substring(fileGet.lastIndexOf("."));

						if (fileGet.lastIndexOf("/") > fileGet.lastIndexOf(".")) {
							fileGet += fileExtension;
							// System.out.println("File created: " + fileGet + fileExtension);
						} else {
							System.out.println("WARNING: File '" + fileGet + "' ends with '" + fileTypeTemp + "' instead of '"
									+ fileExtension + "'");
							fileGet = fileGet.substring(0, fileGet.length() - fileTypeTemp.length()) + fileExtension;
						}
					} else {
						// cannot create the file
						System.out.println("ERROR: File '" + fileGet + "' cannot be found");
						System.exit(0);
					}
				}
			} else {
				fileGet += fileExtension;
			}
		} else {
			// meaning if it just ends with it lol
			if (fileGet.endsWith(fileExtension) == false) {
				if (createFile) {
					fileGet += fileExtension;
				} else {
					// cannot create the file
					System.out.println("ERROR: File '" + fileGet + "' cannot be found");
					System.exit(0);
				}
			}
		}
		return fileGet;
	}

	public static ArrayList<String> removeComment(ArrayList<String> fileArrayList, String startComment, boolean commentAnywhere) {
		ArrayList<String> doc = new ArrayList<String>();
		for (String line : fileArrayList) {

			// tests to see if the line is too short
			if (line.replaceAll("^\\s+", "").length() < startComment.length()) {
				doc.add(line);
				continue;
			}

			// removes whitespace to test for a comment, but returns with
			// whitespace

			if (line.trim().startsWith(startComment) == false) { // doesn't start with a comment
				if (commentAnywhere == true && line.contains(startComment)) { // has comment within
					line = line.substring(0, line.indexOf(startComment));
					doc.add(line);
				} else { // no presense of the comment
					doc.add(line);
				}
			}
		}
		return doc;
	}

	// Removes comment blocks
	public static ArrayList<String> removeCommentBlock(ArrayList<String> fileArrayList, String startComment, String endComment) {
		ArrayList<String> doc = new ArrayList<String>();
		boolean commentBlock = false;

		for (String line : fileArrayList) {
			if (line.trim().length() >= startComment.length()
					&& line.trim().substring(0, startComment.length()).equals(startComment)) {
				commentBlock = true;
			}

			if (commentBlock == false) {
				doc.add(line);
			}

			if (line.trim().length() >= endComment.length() && line.trim().substring(0, endComment.length()).equals(endComment)) {
				commentBlock = false;
			}

		}
		return doc;
	}

	// Skip lines encapsulation
	public static ArrayList<String> removeSkipLineBlock(ArrayList<String> fileArrayList, String startSkip, String endSkip,
			String midSkip) {
		ArrayList<String> doc = new ArrayList<String>();
		boolean skipLineBlock = false;
		String lineCalc = null;

		for (String line : fileArrayList) {
			if (line.trim().length() >= startSkip.length() && line.trim().substring(0, startSkip.length()).equals(startSkip)) {
				skipLineBlock = true;
				lineCalc = null;
				continue;
			}

			if (line.trim().length() >= midSkip.length() && line.trim().substring(0, midSkip.length()).equals(midSkip)) {
				doc.add(lineCalc);
				lineCalc = null;
				continue;
			}

			if (line.trim().length() >= endSkip.length() && line.trim().substring(0, endSkip.length()).equals(endSkip)) {
				skipLineBlock = false;
				doc.add(lineCalc);
				continue;
			}

			if (skipLineBlock == true) {
				if (lineCalc == null) {
					lineCalc = line;
				} else {
					lineCalc = lineCalc + line.replaceAll("^\\s+", "");
				}
			} else {
				doc.add(line);
			}

		}

		return doc;
	}

	public static ArrayList<File> getFilesInFolder(final File folder, final String fileExtension) {
		ArrayList<File> fileArray = new ArrayList<File>();

		for (final File fileEntry : folder.listFiles()) {
			if (fileEntry.getName().endsWith(fileExtension)) {
				fileArray.add(fileEntry);
			}
		}

		return fileArray;
	}

	public static ArrayList<File> getAllFiles(final File folder, final String fileExtension) {
		ArrayList<File> fileArray = new ArrayList<File>();

		for (final File fileEntry : folder.listFiles()) {
			if (fileEntry.isDirectory()) {
				fileArray.addAll(getAllFiles(fileEntry, fileExtension));
			} else {
				if (fileEntry.getName().endsWith(fileExtension)) {
					fileArray.add(fileEntry);
				}
			}
		}

		return fileArray;
	}
	
	public static void deleteDir(File file) {
	    File[] contents = file.listFiles();
	    if (contents != null) {
	        for (File f : contents) {
	            deleteDir(f);
	        }
	    }
	    file.delete();
	}
	
	// Checks for directory
	/*
	public static void checkDir(File pathName, String varPathName) {
		if (pathName == null) {
			System.out.println("WARNING: Directory " + varPathName + " was not found in the .ccu file");
		} else {
			if (pathName.exists() == false) {
				System.out.println("ERROR: Directory " + pathName.toString() + " does not exist");
				System.exit(0);
			} else {
				if (pathName.isDirectory() == false) {
					System.out.println("ERROR: " + pathName.toString() + " is not a directory");
					System.exit(0);
				} else {
					System.out.println("Directory found: " + pathName.toString());
				}
			}
		}
	}*/
}
