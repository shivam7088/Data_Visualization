import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;
import java.util.Map;

@RestController
@RequestMapping("/api/reports")
@CrossOrigin(origins = "http://localhost:3000") // Allow React to connect
public class ReportController {

    private final String PYTHON_SERVICE_URL = "http://localhost:5001/api/visualize/dynamic";

    @GetMapping("/generate")
    public ResponseEntity<?> getDynamicReport(
            @RequestParam String table, 
            @RequestParam String xAxis,
            @RequestParam(required = false) String hue) {
        
        RestTemplate restTemplate = new RestTemplate();
        
        // Construct the URL for the Python Microservice
        StringBuilder urlBuilder = new StringBuilder(PYTHON_SERVICE_URL);
        urlBuilder.append("?table=").append(table);
        urlBuilder.append("&x_axis=").append(xAxis);
        if (hue != null) {
            urlBuilder.append("&hue=").append(hue);
        }

        try {
            // Call Python and return the JSON (containing the base64 image) to React
            Map<String, Object> response = restTemplate.getForObject(urlBuilder.toString(), Map.class);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.status(500).body("Error connecting to Python Visualization Service: " + e.getMessage());
        }
    }
}
