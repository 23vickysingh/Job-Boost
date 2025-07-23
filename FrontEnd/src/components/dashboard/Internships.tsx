
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Bookmark, Calendar, MapPin, ArrowRight } from "lucide-react";

const Internships = () => {
  // Mock data for internships
  interface Internship {
    id: number;
    title: string;
    company: string;
    location: string;
    deadline: string;
    duration: string;
    stipend: string;
    tags: string[];
    isNew?: boolean;
  }

  const internships: Internship[] = [];

  return (
    <Card className="mb-6">
      <CardHeader className="pb-4 flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-xl font-semibold">Internship Opportunities</CardTitle>
          <CardDescription>Available internships matching your profile</CardDescription>
        </div>
        <Button variant="ghost" className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300">
          View All
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-4">
          {internships.map((internship) => (
            <div key={internship.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-gray-900 dark:text-white">{internship.title}</h3>
                    {internship.isNew && (
                      <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
                        New
                      </Badge>
                    )}
                  </div>
                  <p className="text-gray-600 dark:text-gray-300">{internship.company}</p>
                </div>
                <Button variant="ghost" size="sm" className="text-gray-600 dark:text-gray-300">
                  <Bookmark className="h-4 w-4" />
                </Button>
              </div>
              
              <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm text-gray-600 dark:text-gray-300">
                <div className="flex items-center gap-1">
                  <MapPin className="h-4 w-4 text-gray-500" />
                  <span>{internship.location}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Calendar className="h-4 w-4 text-gray-500" />
                  <span>Apply by: {new Date(internship.deadline).toLocaleDateString()}</span>
                </div>
                <div><span className="font-medium">Duration:</span> {internship.duration}</div>
                <div><span className="font-medium">Stipend:</span> {internship.stipend}</div>
              </div>
              
              <div className="mt-3 flex flex-wrap gap-2">
                {internship.tags.map((tag, index) => (
                  <Badge key={index} variant="secondary" className="bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">
                    {tag}
                  </Badge>
                ))}
              </div>
              
              <div className="mt-4 flex justify-end">
                <Button size="sm">Apply Now</Button>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default Internships;
