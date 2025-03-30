
import re
from collections import Counter
from typing import Dict, Any
import json

class LogAnalyzer:
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path
        self.results = {
            "404_urls": Counter(),
            "response_times": [],
            "db_tables": Counter(),
            "redirects": Counter(),
            "server_errors": Counter(),
        }

    def analyze(self) -> None:
        patterns = {
            "404": re.compile(r'path="([^"]+)"[^ ]+status=404'),
            "response_time": re.compile(r'status=200[^ ]* service=(\d+)ms'),
            "db_query": re.compile(r'FROM\s+"([^"]+)"', re.IGNORECASE),
            "redirect": re.compile(r'path="([^"]+)"[^ ]+status=(301|302)'),
            "server_error": re.compile(r'path="([^"]+)"[^ ]+status=5\d{2}'),
        }

        with open(self.log_file_path, "r", encoding="utf-8") as file:
            for line in file:
                if match := patterns["404"].search(line):
                    self.results["404_urls"][match.group(1)] += 1
                if match := patterns["response_time"].search(line):
                    self.results["response_times"].append(int(match.group(1)))
                if match := patterns["db_query"].search(line):
                    self.results["db_tables"][match.group(1)] += 1
                if match := patterns["redirect"].search(line):
                    self.results["redirects"][match.group(1)] += 1
                if match := patterns["server_error"].search(line):
                    self.results["server_errors"][match.group(1)] += 1

    def generate_report(self) -> Dict[str, Any]:
        avg_time = (
            sum(self.results["response_times"]) / len(self.results["response_times"])
            if self.results["response_times"]
            else None
        )
        most_common_table = self.results["db_tables"].most_common(1)[0] if self.results["db_tables"] else None

        return {
            "404_urls": dict(self.results["404_urls"]),
            "avg_response_time_ms": avg_time,
            "most_frequent_table": most_common_table,
            "redirects": dict(self.results["redirects"]),
            "server_errors": dict(self.results["server_errors"]),
        }

def save_report_to_file(report: Dict[str, Any], filename: str = "report.json") -> None:
    """Saves the report to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f" Report saved to '{filename}'")

if __name__ == "__main__":
    analyzer = LogAnalyzer("2014-09-03.log")
    analyzer.analyze()
    report = analyzer.generate_report()

    # Print to console
    print(json.dumps(report, indent=2))

    # Save to a file (JSON format)
    save_report_to_file(report, "report.json")

    # Save as a .txt file
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write("Log Analysis Report\n")
        f.write("=" * 40 + "\n")
        f.write(f"1. 404 URLs: {len(report['404_urls'])} found\n")
        for url, count in report["404_urls"].items():
            f.write(f"   - {url}: {count} times\n")
        f.write(f"\n2. Avg Response Time: {report['avg_response_time_ms']} ms\n")
        f.write(f"\n3. Most Frequent Table: {report['most_frequent_table']}\n")
        f.write(f"\n4. Redirects: {len(report['redirects'])} found\n")
        for url, count in report['redirects'].items():
            f.write(f"   - {url}: {count} times\n")
        f.write(f"\n5. Server Errors: {len(report['server_errors'])} found\n")
        for url, count in report['server_errors'].items():
            f.write(f"   - {url}: {count} times\n")
    print(" Report saved to 'report.txt'")