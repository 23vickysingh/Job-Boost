
import React, { useState } from 'react';
import { 
  Card, 
  CardContent
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { 
  Plus, 
  Check, 
  Bookmark,
  ArrowRight 
} from "lucide-react";

// Mock data for the job matches
const initialJobMatches: any[] = [];

const JobMatchesList: React.FC = () => {
  const [jobMatches, setJobMatches] = useState(initialJobMatches);
  const [applications, setApplications] = useState<any[]>([]);
  
  const applyToJob = (jobId: number) => {
    setJobMatches(prev => 
      prev.map(job => 
        job.id === jobId ? { ...job, applied: true } : job
      )
    );
    
    // Add to applications
    const job = jobMatches.find(j => j.id === jobId);
    if (job) {
      const newApplication = {
        id: Date.now(),
        title: job.title,
        company: job.company,
        appliedDate: new Date().toISOString().split('T')[0],
        status: "Applied",
        response: false
      };
      setApplications(prev => [newApplication, ...prev]);
    }
  };

  return (
    <>
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
          Recommended Jobs for You
        </h2>
        <Button variant="ghost" className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300">
          View All
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {jobMatches.map(job => (
          <Card key={job.id} className={job.applied ? "opacity-75" : ""}>
            <CardContent className="p-6">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-lg text-gray-900 dark:text-white">
                    {job.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300">{job.company}</p>
                </div>
                <div className="bg-blue-100 dark:bg-blue-900/30 px-2 py-1 rounded-full">
                  <span className="text-blue-700 dark:text-blue-300 font-semibold">
                    {job.matchScore}% Match
                  </span>
                </div>
              </div>
              
              <div className="mt-4 space-y-2">
                <div className="flex items-center text-gray-600 dark:text-gray-300 text-sm">
                  <span className="font-medium mr-2">Location:</span> {job.location}
                </div>
                <div className="flex items-center text-gray-600 dark:text-gray-300 text-sm">
                  <span className="font-medium mr-2">Salary:</span> {job.salary}
                </div>
                <div className="flex items-center text-gray-600 dark:text-gray-300 text-sm">
                  <span className="font-medium mr-2">Posted:</span> {job.posted}
                </div>
              </div>
              
              <div className="mt-4 flex justify-between">
                <Button 
                  variant="outline" 
                  size="sm"
                  className="text-gray-600 dark:text-gray-300"
                >
                  <Bookmark className="mr-2 h-4 w-4" />
                  Save
                </Button>
                
                <Button
                  size="sm"
                  disabled={job.applied}
                  onClick={() => applyToJob(job.id)}
                >
                  {job.applied ? (
                    <>
                      <Check className="mr-2 h-4 w-4" />
                      Applied
                    </>
                  ) : (
                    <>
                      <Plus className="mr-2 h-4 w-4" />
                      Apply Now
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
      
      <div className="flex justify-center mt-8">
        <Button className="flex items-center">
          Find More Matches
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </>
  );
};

export default JobMatchesList;
