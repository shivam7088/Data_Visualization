import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;
import java.util.Map;

@RestController
@RequestMapping("/api/reports")
public class ReportController {

    @GetMapping("/{type}")
    public ResponseEntity<?> getReport(@PathVariable String type) {
        // Python service URL
        String pythonUrl = "http://localhost:5001/api/visualize?table=" + type + "&column=status";
        
        RestTemplate restTemplate = new RestTemplate();
        try {
            // Forward the request to Python and return the response to React
            Map<String, Object> response = restTemplate.getForObject(pythonUrl, Map.class);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.status(500).body("Error contacting visualization service");
        }
    }
}