package TestX;

import com.techventus.server.voice.Voice;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import java.io.File;
 
public class ReadXML {
 
	public static void main(String argv[]) {
              String userName="albertosantos275@gmail.com";
              String pass= "luidor275";
              String originNumber = "7182183571";  
              String destinationNumber = "3474216519";
 
	  try {
 
		File fXmlFile = new File("C:\\testfile.xml");
		DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
		Document doc = dBuilder.parse(fXmlFile);
		doc.getDocumentElement().normalize();
 
		//JAXBContext jc = JAXBContext.newInstance("my.package.name"); 

                //Unmarshaller unmarshaller = jc.createUnmarshaller(); 

                 //MyFile myFile = (MyFile) unmarshaller.unmarshal(new File( "myFile.xml"));
                
                
                System.out.println("Test :" + doc.getDocumentElement().getNodeName());
		NodeList nList = doc.getElementsByTagName("student");
		System.out.println("-----------------------");
 
		for (int temp = 0; temp < nList.getLength(); temp++) {
 
		   Node nNode = nList.item(temp);
		   if (nNode.getNodeType() == Node.ELEMENT_NODE) {
 
		      Element eElement = (Element) nNode;
 
		      System.out.println("First Name : " + getTagValue("firstname", eElement));
		      System.out.println("Last Name : " + getTagValue("lastname", eElement));
	              
 
		   }
		}
                      System.out.println("running");
                      Voice v1 = new Voice(userName,pass);
                      v1.sendSMS("3474216519", "test message");
	  } 
                catch (Exception e) 
                {
		e.printStackTrace();
                }
  }
 
  private static String getTagValue(String sTag, Element eElement) {
	NodeList nlList = eElement.getElementsByTagName(sTag).item(0).getChildNodes();
 
        Node nValue = (Node) nlList.item(0);
 
	return nValue.getNodeValue();
  }
 
}