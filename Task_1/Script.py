import re
import json
from collections import Counter
from typing import Dict, Any


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
        self.patterns = {
            "router_404": re.compile(r'path="([^"]+)"[^ ]*.*status=404'),
            "router_redirect": re.compile(r'path="([^"]+)"[^ ]*.*status=(301|302)'),
            "router_server_error": re.compile(r'path="([^"]+)"[^ ]*.*status=5\d{2}'),
            "router_response_time": re.compile(r'service=(\d+)ms'),
            "app_db_query": re.compile(r'FROM\s+"?(\w+)"?', re.IGNORECASE),
        }

    def analyze(self) -> None:
        try:
            with open(self.log_file_path, "r", encoding="utf-8") as file:
                for line in file:
                    if "heroku/router" in line:
                        self._analyze_router_line(line)
                    elif "app/web" in line:
                        self._analyze_app_line(line)
        except FileNotFoundError:
            print(f"Error: Log file '{self.log_file_path}' not found.")
        except Exception as e:
            print(f"An error occurred while analyzing the log: {e}")

    def _analyze_router_line(self, line: str) -> None:
        if match := self.patterns["router_404"].search(line):
            self.results["404_urls"][match.group(1)] += 1
        elif match := self.patterns["router_redirect"].search(line):
            self.results["redirects"][match.group(1)] += 1
        elif match := self.patterns["router_server_error"].search(line):
            self.results["server_errors"][match.group(1)] += 1

        if match := self.patterns["router_response_time"].search(line):
            self.results["response_times"].append(int(match.group(1)))

    def _analyze_app_line(self, line: str) -> None:
        if match := self.patterns["app_db_query"].search(line):
            self.results["db_tables"][match.group(1)] += 1

    def generate_report(self) -> Dict[str, Any]:
        avg_time = (
            sum(self.results["response_times"]) / len(self.results["response_times"])
            if self.results["response_times"]
            else None
        )
        most_common_table = (
            {"table": table, "count": count}
            for table, count in self.results["db_tables"].most_common(1)
        )
        most_common_table = next(most_common_table, None)

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
    print(f"Report saved to '{filename}'")


def save_report_as_text(report: Dict[str, Any], filename: str = "report.txt") -> None:
    """Saves the report to a plain text file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Log Analysis Report\n")
        f.write("=" * 40 + "\n\n")

        f.write(f"1. 404 URLs ({len(report['404_urls'])} found):\n")
        for url, count in report["404_urls"].items():
            f.write(f"   - {url}: {count} times\n")
        
        f.write(f"\n2. Average Response Time: {report['avg_response_time_ms']:.2f} ms\n" if report['avg_response_time_ms'] else "\n2. Average Response Time: No data\n")
        
        if report["most_frequent_table"]:
            f.write(f"\n3. Most Frequent Table: {report['most_frequent_table']['table']} ({report['most_frequent_table']['count']} queries)\n")
        else:
            f.write("\n3. Most Frequent Table: No data\n")

        f.write(f"\n4. Redirects ({len(report['redirects'])} found):\n")
        for url, count in report['redirects'].items():
            f.write(f"   - {url}: {count} times\n")
        
        f.write(f"\n5. Server Errors ({len(report['server_errors'])} found):\n")
        for url, count in report['server_errors'].items():
            f.write(f"   - {url}: {count} times\n")

    print(f"Report saved to '{filename}'")


if __name__ == "__main__":
    analyzer = LogAnalyzer("2014-09-03.log")
    analyzer.analyze()
    report = analyzer.generate_report()

    # Print nicely in console
    print(json.dumps(report, indent=2))

    # Save to files
    save_report_to_file(report, "report.json")
    save_report_as_text(report, "report.txt")
