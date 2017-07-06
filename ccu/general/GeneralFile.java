package ccu.general;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;

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
		System.out.println("ERROR: Unknown");
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
			System.out.println("(Unknown) ERROR: Could not find the file: \n" + e);
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
		ArrayList<String> returnArray = GeneralFile.removeSkipLineBlock(
				GeneralFile.removeComment(GeneralFile.removeCommentBlock(getArray, "//=", "=//"), "//"), "/*", "*/");
		return returnArray;
	}

	public static String checkFileExtension(String fileGet, String fileExtension) {
		if (fileGet.contains(".")) {
			if (fileGet.substring(fileGet.lastIndexOf(".")).equals(fileExtension)) {
				// success
				// System.out.println("File created: '" + fileGet + "'");
			} else {
				String fileTypeTemp = fileGet.substring(fileGet.lastIndexOf("."));
				if (fileGet.lastIndexOf("/") > fileGet.lastIndexOf(".")) {
					fileGet += fileExtension;
					// System.out.println("File created: " + fileGet + fileExtension);
				} else {
					System.out.println(
							"WARNING: File '" + fileGet + "' ends with '" + fileTypeTemp + "' instead of '" + fileExtension + "'");
					fileGet = fileGet.substring(0, fileGet.length() - fileTypeTemp.length()) + fileExtension;
				}
			}
		} else {
			fileGet += fileExtension;
		}

		return fileGet;
	}

	public static ArrayList<String> removeComment(ArrayList<String> fileArrayList, String startComment) {
		ArrayList<String> doc = new ArrayList<String>();
		for (String line : fileArrayList) {

			// tests to see if the line is too short
			if (line.replaceAll("^\\s+", "").length() < startComment.length()) {
				doc.add(line);
				continue;
			}

			// removes whitespace to test for a comment, but returns with
			// whitespace
			String lineSave = line;
			line = line.trim();

			if (line.length() >= startComment.length() && line.substring(0, startComment.length()).equals(startComment) == false) {
				doc.add(lineSave);
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
	public static ArrayList<String> removeSkipLineBlock(ArrayList<String> fileArrayList, String startSkip, String endSkip) {
		ArrayList<String> doc = new ArrayList<String>();
		boolean skipLineBlock = false;
		String lineCalc = null;

		for (String line : fileArrayList) {
			if (line.trim().length() >= startSkip.length() && line.trim().substring(0, startSkip.length()).equals(startSkip)) {
				skipLineBlock = true;
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
