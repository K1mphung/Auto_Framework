"""
TestNG Suite Runner
Executes tests based on TestNG XML configuration
Bridges TestNG XML configuration with PyTest execution
"""

import xml.etree.ElementTree as ET
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Set
from utilities.logger_config import LoggerConfig


class TestNGSuiteRunner:
    """
    Runs TestNG test suites using PyTest
    Reads TestNG XML configuration and executes tests accordingly
    """
    
    def __init__(self, testng_xml_path: str = "testng.xml"):
        """
        Initialize TestNG Suite Runner
        
        Args:
            testng_xml_path: Path to testng.xml file
        """
        self.logger = LoggerConfig.get_logger(__name__)
        self.xml_path = Path(testng_xml_path)
        self.test_suites = []
        self.parse_testng_xml()
    
    def parse_testng_xml(self):
        """Parse TestNG XML configuration file"""
        try:
            if not self.xml_path.exists():
                self.logger.error(f"TestNG XML file not found: {self.xml_path}")
                return
            
            tree = ET.parse(self.xml_path)
            root = tree.getroot()
            
            # Extract suite parameters
            self.suite_parameters = {}
            for param in root.findall('.//parameter'):
                self.suite_parameters[param.get('name')] = param.get('value')
            
            # Extract tests
            for test_elem in root.findall('.//test'):
                test_data = {
                    'name': test_elem.get('name'),
                    'enabled': test_elem.get('enabled', 'true').lower() == 'true',
                    'groups': [],
                    'classes': [],
                    'methods': []
                }
                
                # Extract groups
                for group in test_elem.findall('.//include'):
                    test_data['groups'].append(group.get('name'))
                
                # Extract classes and methods
                for class_elem in test_elem.findall('.//class'):
                    class_name = class_elem.get('name')
                    methods = []
                    
                    for method in class_elem.findall('.//include'):
                        methods.append(method.get('name'))
                    
                    test_data['classes'].append(class_name)
                    if methods:
                        test_data['methods'].extend([f"{class_name}::{m}" for m in methods])
                
                self.test_suites.append(test_data)
            
            self.logger.info(f"Parsed {len(self.test_suites)} test suites from TestNG XML")
            
        except Exception as e:
            self.logger.error(f"Error parsing TestNG XML: {str(e)}")
    
    def run_suite(self, suite_name: str = None, verbose: bool = True) -> int:
        """
        Run a specific test suite
        
        Args:
            suite_name: Name of suite to run (None = run all)
            verbose: Verbose output
            
        Returns:
            int: Exit code from pytest
        """
        try:
            # Filter suites
            suites_to_run = self.test_suites
            if suite_name:
                suites_to_run = [s for s in self.test_suites if s['name'] == suite_name]
                
                if not suites_to_run:
                    self.logger.error(f"Suite '{suite_name}' not found in TestNG XML")
                    return 1
            
            # Build pytest command
            pytest_args = self._build_pytest_args(suites_to_run, verbose)
            
            self.logger.info(f"Running {len(suites_to_run)} suite(s)...")
            self.logger.info(f"Command: pytest {' '.join(pytest_args)}")
            
            # Execute pytest
            result = subprocess.run(
                ['pytest'] + pytest_args,
                cwd='src/test/python'
            )
            
            return result.returncode
            
        except Exception as e:
            self.logger.error(f"Error running test suite: {str(e)}")
            return 1
    
    def run_group(self, group_name: str) -> int:
        """
        Run tests by group name
        
        Args:
            group_name: Group name to run
            
        Returns:
            int: Exit code from pytest
        """
        try:
            self.logger.info(f"Running tests in group: {group_name}")
            
            # Build pytest command with group marker
            pytest_args = ['tests', '-m', group_name, '-v']
            
            self.logger.info(f"Command: pytest {' '.join(pytest_args)}")
            
            result = subprocess.run(
                ['pytest'] + pytest_args,
                cwd='src/test/python'
            )
            
            return result.returncode
            
        except Exception as e:
            self.logger.error(f"Error running group: {str(e)}")
            return 1
    
    def run_parallel(self, num_workers: int = 4) -> int:
        """
        Run tests in parallel
        
        Args:
            num_workers: Number of parallel workers
            
        Returns:
            int: Exit code from pytest
        """
        try:
            self.logger.info(f"Running tests in parallel with {num_workers} workers")
            
            pytest_args = [
                'tests',
                '-v',
                '-n', str(num_workers),
                '--html=../../../reports/report.html',
                '--self-contained-html'
            ]
            
            result = subprocess.run(
                ['pytest'] + pytest_args,
                cwd='src/test/python'
            )
            
            return result.returncode
            
        except Exception as e:
            self.logger.error(f"Error running parallel tests: {str(e)}")
            return 1
    
    def _build_pytest_args(self, suites: List[Dict], verbose: bool = True) -> List[str]:
        """
        Build pytest command line arguments from test suites
        
        Args:
            suites: Test suites to run
            verbose: Verbose output flag
            
        Returns:
            List of pytest arguments
        """
        args = ['tests']
        
        if verbose:
            args.append('-v')
        
        # Add markers for groups
        all_groups = set()
        for suite in suites:
            if suite.get('groups'):
                all_groups.update(suite['groups'])
        
        if all_groups:
            marker_expr = ' or '.join(all_groups)
            args.extend(['-m', marker_expr])
        
        # Add HTML report
        args.extend([
            '--html=../../../reports/report.html',
            '--self-contained-html',
            '--cov=src/test/python',
            '--cov-report=html:../../../reports/coverage'
        ])
        
        return args
    
    def list_suites(self):
        """List all available test suites"""
        self.logger.info("Available Test Suites:")
        print("\n" + "="*70)
        
        for i, suite in enumerate(self.test_suites, 1):
            status = "ENABLED" if suite['enabled'] else "DISABLED"
            print(f"\n{i}. {suite['name']} [{status}]")
            print(f"   Groups: {', '.join(suite['groups']) or 'None'}")
            print(f"   Classes: {', '.join(suite['classes'])}")
            if suite['methods']:
                print(f"   Methods: {len(suite['methods'])} test(s)")
        
        print("\n" + "="*70)
    
    def get_suite_info(self, suite_name: str) -> Dict:
        """Get information about a specific suite"""
        for suite in self.test_suites:
            if suite['name'] == suite_name:
                return suite
        return None
    
    def run_by_priority(self, priority: int) -> int:
        """
        Run tests by priority
        
        Args:
            priority: Priority level (0-10, 0 is highest)
            
        Returns:
            int: Exit code from pytest
        """
        try:
            self.logger.info(f"Running tests with priority: {priority}")
            
            # Would need to track priority in test registry
            # For now, just log
            self.logger.warning("Priority-based execution requires test metadata collection")
            
            return 1
            
        except Exception as e:
            self.logger.error(f"Error running by priority: {str(e)}")
            return 1


def main():
    """Main entry point for TestNG Suite Runner"""
    import sys
    
    logger = LoggerConfig.get_logger(__name__)
    runner = TestNGSuiteRunner()
    
    if len(sys.argv) < 2:
        runner.list_suites()
        print("\nUsage:")
        print("  python -m utilities.testng_suite_runner list")
        print("  python -m utilities.testng_suite_runner run <suite_name>")
        print("  python -m utilities.testng_suite_runner group <group_name>")
        print("  python -m utilities.testng_suite_runner parallel [num_workers]")
        return 0
    
    command = sys.argv[1]
    
    if command == 'list':
        runner.list_suites()
        return 0
    
    elif command == 'run':
        if len(sys.argv) < 3:
            runner.list_suites()
            return 1
        
        suite_name = sys.argv[2]
        return runner.run_suite(suite_name)
    
    elif command == 'group':
        if len(sys.argv) < 3:
            logger.error("Specify group name")
            return 1
        
        group_name = sys.argv[2]
        return runner.run_group(group_name)
    
    elif command == 'parallel':
        num_workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
        return runner.run_parallel(num_workers)
    
    else:
        logger.error(f"Unknown command: {command}")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
