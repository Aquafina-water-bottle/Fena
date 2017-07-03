package ccu.mcfunction;

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

			String mcfunctionFile = null;

			/* spellchecks for the file extension
			 * if file is asdf.notmcfunction
			 * 	-removes .notmcfunction and replaces it with .mcfunction
			 *  -displays WARNING
			 * if file is asdf
			 *  -adds .mcfunction
			 * if file is asdf.mcfunction
			 *  -does nothing woot woot
			 */

			if (functionArray[0].contains(".")) {
				if (functionArray[0].substring(functionArray[0].lastIndexOf(".")).equals(".mcfunction")) {
					mcfunctionFile = functionArray[0];
					System.out.println("File created: '" + functionArray[0] + "'");
				} else {
					String fileTypeTemp = functionArray[0].substring(functionArray[0].lastIndexOf("."));
					System.out
							.println("WARNING: File '" + functionArray[0] + "' ends with '" + fileTypeTemp + "' instead of '.mcfunction'");
					mcfunctionFile = functionArray[0].substring(0, functionArray[0].length() - fileTypeTemp.length()) + ".mcfunction";
					System.out.println("File created: '" + functionArray[0].substring(0, functionArray[0].length() - fileTypeTemp.length())
							+ ".mcfunction'");
				}
			} else {
				mcfunctionFile = functionArray[0] + ".mcfunction";
				System.out.println("File created: " + functionArray[0] + ".mcfunction");
			}

			Cmd_MFunc.arrayMFuncNameSave.add(mcfunctionFile.replace(".mcfunction", ""));

			PrintWriter writer = null;

			// TODO spaces are replaced with %20?
			// specifically in the commands

			try {
				writer = new PrintWriter(Var_Options.filePathFuncOption + "/" + mcfunctionFile, "UTF-8");
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
