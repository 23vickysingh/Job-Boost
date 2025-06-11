
import React from 'react';
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle, 
  CardDescription 
} from "@/components/ui/card";
import { PieChart, BarChart } from "lucide-react";

const AnalyticsDashboard: React.FC = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Application Stats</CardTitle>
          <CardDescription>
            Your job application performance
          </CardDescription>
        </CardHeader>
        <CardContent className="h-80 flex items-center justify-center">
          <div className="text-center space-y-2">
            <PieChart className="h-16 w-16 mx-auto text-blue-600 dark:text-blue-400" />
            <p className="text-gray-600 dark:text-gray-300">
              Analytics visualization would appear here
            </p>
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>Response Timeline</CardTitle>
          <CardDescription>
            Average response times from employers
          </CardDescription>
        </CardHeader>
        <CardContent className="h-80 flex items-center justify-center">
          <div className="text-center space-y-2">
            <BarChart className="h-16 w-16 mx-auto text-blue-600 dark:text-blue-400" />
            <p className="text-gray-600 dark:text-gray-300">
              Timeline visualization would appear here
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AnalyticsDashboard;
