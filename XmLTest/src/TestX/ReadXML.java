package TestX;

import com.techventus.server.voice.Voice;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import java.io.File;
import java.io.*;
 
public class ReadXML {
 
	public static void main(String argv[]) {
              String userName="albertosantos275@gmail.com";
              String pass= "luidor275";
              String originNumber = "7182183571";  
              String destinationNumber = "3474216519,3472761475";
            
        //boolean exists = true;
        //while(exists){
 
	  try {
              boolean condition = true;
              while(condition){
		
                  File fXmlFile = new File("C:\\testfile.xml");
                  boolean exists_2 = fXmlFile.exists(); // declare variable and initialize to existing
                  
                  //check if file is there, otherwise keep checking
                  if (!exists_2)
                  {
                     System.out.println(" File is not there. Keep checking:" + exists_2);
                     //exists_2 = false;
                     Thread.sleep(5000); // wait 5 seconds before checking again
                     
                  }
                  // if file is there, read it 
                  else
                  {
                
                      
                    // Parsing Routine
                    DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
                    DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
                    Document doc = dBuilder.parse(fXmlFile);
                    doc.getDocumentElement().normalize();
 
		//JAXBContext jc = JAXBContext.newInstance("my.package.name"); 

                //Unmarshaller unmarshaller = jc.createUnmarshaller(); 

                 //MyFile myFile = (MyFile) unmarshaller.unmarshal(new File( "myFile.xml"));
                
                    System.out.println("---------------------------------------------------------");
                    System.out.println("Test : " + doc.getDocumentElement().getNodeName());
                    NodeList nList = doc.getElementsByTagName("student");
                    System.out.println("---------------------------------------------------------");
 
		        // getting every object from the Xml File
                        for (int temp = 0; temp < nList.getLength(); temp++) 
                        {
 
                            Node nNode = nList.item(temp);
                            if (nNode.getNodeType() == Node.ELEMENT_NODE) 
                            {
                       
 
                                Element eElement = (Element) nNode;
                                
                                // Printing objects

                                System.out.println("First Name : " + getTagValue("firstname", eElement));
                                System.out.println("Last Name  : " + getTagValue("lastname", eElement));
                                System.out.println("---------------------------------------------------------");
                        
                            }
                   // once file is printed, execute message routine
                    System.out.println("File is there. Message routine is about to execute:" + exists_2);
                    System.out.println("Running");
                    Voice v1 = new Voice(userName,pass);
                    v1.sendSMS("3474216519,3472761475", "Test message");
                  
		} 
                        System.out.println("Done");
                        condition = false; // condition must change to false to not run infinite loop
                        //System.out.println("Done");
                  }        
               //boolean noexists = true;
               //boolean exists = fXmlFile.exists();
  
                       // while(!exists) { // loop until  file is there 
                        //System.out.println(" File is not there. Keep checking:" + exists);
                        //Thread.sleep(5000);
                        //exists=true;
                        //exists = fXmlFile.exists(); //check to see if your file is there 
                        //System.out.println(" File is not there. Keep checking:" + exists);
                        //Thread.sleep(5000);//
                       
                        }
                        
                       // else{
                        
                        //System.out.println("File is there. Message routine is about to execute:" + exists);
                        //System.out.println("Running");
                        //Voice v1 = new Voice(userName,pass);
                        //v1.sendSMS("3474216519", "test message");
                        
                        
	                
             
          }
                catch (Exception e) 
                {
		//e.printStackTrace();
                 System.out.println("File not found");
                }
  //exists = false;
        }
        
  private static String getTagValue(String sTag, Element eElement) {
	NodeList nlList = eElement.getElementsByTagName(sTag).item(0).getChildNodes();
 
        Node nValue = (Node) nlList.item(0);
 
	return nValue.getNodeValue();
  }
 
}