package ccu.command;

public class Var_Import {
/** Avaliable parameters:
 * DIRECTORY - to specify that it's a directory rather than a ccu file
 * LIBRARY- to import from a specific library folder (specified in the ini file) - a special 'DIRECTORY'
 * WITHIN - an import file is either within the folder or a folder above
 * GROUPCOORDS - to import only group coordinates from the name_dat.ccu files
 * 
 * LIBRARY should not be used with GROUPCOORDS - all ccu files that aren't specifically meant for importing should be elsewhere
 * LIBRARY cannot work with WITHIN
 * DIRECTORY cannot work with WITHIN
 * 
 * whether the functions / definitions / arrays in the imported files are global depends on the actual file itself
 * aka the funcs / defs / arrays should be specified with "global" themselves
 */
}
