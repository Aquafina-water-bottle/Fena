package ccu.mcfunction;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;

import ccu.command.Cmd_MFunc;
import ccu.command.Var_Options;
import ccu.general.GeneralFile;

public class WriteFile {
	public static void writeMCFunction() {

		for (String[] functionArray : Cmd_MFunc.arrayMFuncSave) {
			if (Var_Options.filePathFuncOption == null) {
				System.out.println("ERROR: 'MFUNC' statement was detected but 'filePathFuncOption' is empty");
				System.exit(0);
			}

			String mcfunctionFile = functionArray[0];
			PrintWriter writer = null;

			// TODO spaces are replaced with %20?
			// specifically in the commands

			// Creates the folder if it wasn't made already

			File folderCreate = new File(mcfunctionFile);
			File folderCalc = new File(folderCreate.getParent().toString());
			try {
				if (folderCalc.mkdirs()) {
					// System.out.println("Directory created:" + folderCalc.toString());
				} else {
					if (folderCalc.isDirectory() && folderCalc.toString().equals("null") == false) {
						// System.out.println("Directory found: " + folderCalc.toString());
					} else {
						System.out.println("ERROR: Directory '" + folderCalc.toString() + "' was not created");
						System.exit(0);
					}
				}
			} catch (Exception e) {
				GeneralFile.dispError(e);
				System.exit(0);
			}

			try {
				writer = new PrintWriter(mcfunctionFile, "UTF-8");
			} catch (FileNotFoundException | UnsupportedEncodingException e) {
				GeneralFile.dispError(e);
				System.exit(0);
			}

			for (int i = 1; i < functionArray.length; i++) {
				writer.println(functionArray[i]);
			}
			writer.close();
		}
	}
}
