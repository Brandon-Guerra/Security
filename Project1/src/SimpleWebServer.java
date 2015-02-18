/********************************************************************************

SimpleWebServer.java


This toy web server is used to illustrate security vulnerabilities.
This web server only supports extremely simple HTTP GET requests.

This code is taken from Foundations of Security by Daswani et. al.
and has been modified by Brandon Guerra.

*******************************************************************************/



import java.io.*;
import java.net.*;
import java.util.*;

public class SimpleWebServer {
	
	/* Run the HTTP server on this TCP port. */
	private static final int PORT = 8080;
	
	/* The socket used to process incoming connections
	   from web clients. */
	private static ServerSocket dServerSocket;
	
	public SimpleWebServer () throws Exception {
		dServerSocket = new ServerSocket (PORT);
	}
	
	public void run() throws Exception {
		while (true) {
			/* Wait for a connection from a client. */
			Socket s = dServerSocket.accept();
			
			/* Then, process the client's request. */
			processRequest(s);
		}
	}

	/* Reads the HTTP request from the client and
	   responds with the file the user requested or
	   an HTTP error code. */
	public void processRequest(Socket s) throws Exception {

		/* Used to read data from the client. */
		BufferedReader br = 
				new BufferedReader (
						new InputStreamReader (s.getInputStream()));
		
		/* Used to write data to the client. */
		OutputStreamWriter osw = 
				new OutputStreamWriter (s.getOutputStream());
		
		/* Read the HTTP request from the client. */
		String request = br.readLine();
		
		String command = null;
		String pathname = null;
		
		/* Parse the HTTP request. */
		StringTokenizer st = 
				new StringTokenizer (request, " ");
		
		command = st.nextToken();
		pathname = st.nextToken();
		
		if (command.equals("GET")) {
			/* If the response is a GET,
			   try to respond with the file
			   the user is requesting. */
			serveFile (osw, pathname);
		}
		
		else if (command.equals("PUT")) {
			/* If the response is a PUT,
			   try to store the file the
			   the user is requesting. */
			storeFile (br, osw, pathname);
		}
		
		else {
			 /*If the request is NOT a GET, 
			   return an error saying this server
			   does not implement the requested command. */
			osw.write(("HTTP/1.0 501 Not Implemented\n\n"));
		}
		
		/* Close the connection to the client. */
		osw.close();
	}
	
	public void serveFile (OutputStreamWriter osw, String pathname) throws Exception {
		
		System.out.println("serve file called");
		FileReader fr = null;
		int c = -1;
		StringBuffer sb = new StringBuffer();
		
		/* Remove the initial slash at the beginning
		   of the pathname in the request. */
		if (pathname.charAt(0) == '/')
			pathname = pathname.substring(1);
		
		/* If there was no filename specified by the
		   client, serve the "index.html" file. */
		if (pathname.equals(""))
			pathname = "index.html";
		
		/* Try to open file specified by the pathname. */
		try {
			fr = new FileReader (pathname);
			c = fr.read();
		}
		catch (Exception e) {
			/* If the file is not found, return the
			   appropriate HTTP response code. */
			osw.write ("HTTP/1.0 404 Not Found\n\n");
			return;
		}
		
		/* If the requested file can be successfully opened
		   and read, then return an OK response code and 
		   send the contents of the file. */
		osw.write ("HTTP/1.0 200 OK\n\n");
		while (c != -1) {
			sb.append((char)c);
			c = fr.read();
		}
		fr.close();
		osw.write (sb.toString());
	}
	
	public void storeFile(BufferedReader br, OutputStreamWriter osw, String pathname) throws Exception {
		
		FileWriter fw = null;
		try {
			fw = new FileWriter (pathname);
			String s = br.readLine();
			while (s != null) {
				fw.write (s);
				s = br.readLine();
			}
			fw.close();
			osw.write ("HTTP/1.0 201 Created");
		}
		catch (Exception e) {
			osw.write ("HTTP/1.0 500 Internal Server Error");
		}
	}
	
	public void logEntry(String filename,String record) throws IOException {

		FileWriter fw = new FileWriter (filename, true);
		fw.write (getTimestamp() + " " + record);
		fw.close();
	}
	
	public String getTimestamp() {

		return (new Date()).toString();
	}
	
	/* This method is called when the program is run from
	   the command line. */
	public static void main (String argv[]) throws Exception {
		
		/* Create a SimpleWebServer object and run it. */
		SimpleWebServer sws = new SimpleWebServer();
		sws.run();
	}
}