
import React, { useState } from 'react';
import { 
  Card, 
  CardContent
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { 
  Plus, 
  Check, 
  Bookmark,
  ExternalLink,
  MapPin,
  Building,
  Calendar,
  Clock,
  X,
  CheckCircle
} from "lucide-react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchJobMatches, updateJobMatchStatus, deleteJobMatch } from "@/lib/api";
import { formatDistanceToNow, parseISO } from "date-fns";
import { useJobs, type JobMatch } from "@/contexts/JobContext";
import { toast } from "sonner";

const JobMatchesList: React.FC = () => {
  // Get job management functions from context
  const { addToApplications, removeJobMatch, isJobApplied, isJobRemoved } = useJobs();
  
  // State for confirmation dialog
  const [showNotInterestedDialog, setShowNotInterestedDialog] = useState(false);
  const [selectedJobMatch, setSelectedJobMatch] = useState<JobMatch | null>(null);
  
  // Get query client for cache invalidation
  const queryClient = useQueryClient();
  
  // Fetch job matches from API
  const { data: jobMatchesResponse, error } = useQuery({
    queryKey: ["jobMatches"],
    queryFn: () => fetchJobMatches({ limit: 10 }),
  });

  const jobMatches: JobMatch[] = jobMatchesResponse?.data || [];

  const formatRelevanceScore = (score: number): string => {
    return `${Math.round(score * 100)}%`;
  };

  const formatJobPostedDate = (dateString?: string): string => {
    if (!dateString) return "Date not available";
    try {
      const date = parseISO(dateString);
      return formatDistanceToNow(date, { addSuffix: true });
    } catch {
      return "Date not available";
    }
  };

  const getEmploymentTypeColor = (type?: string): string => {
    switch (type?.toLowerCase()) {
      case 'fulltime':
      case 'full-time':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
      case 'parttime':
      case 'part-time':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300';
      case 'contract':
      case 'contractor':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300';
      case 'intern':
      case 'internship':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300';
    }
  };

  const getRelevanceColor = (score: number): string => {
    if (score >= 0.8) return 'text-green-600 dark:text-green-400 font-bold';
    if (score >= 0.6) return 'text-orange-600 dark:text-orange-400 font-semibold';
    return 'text-red-600 dark:text-red-400';
  };

  const handleApplyClick = (applyLink?: string) => {
    if (applyLink) {
      window.open(applyLink, '_blank', 'noopener,noreferrer');
    }
  };

  // Handler for moving job to applications
  const handleMoveToApplications = async (jobMatch: JobMatch) => {
    try {
      await addToApplications(jobMatch);
      // Invalidate and refetch related queries
      queryClient.invalidateQueries({ queryKey: ["jobMatches"] });
      queryClient.invalidateQueries({ queryKey: ["jobMatchStats"] });
      queryClient.invalidateQueries({ queryKey: ["applications"] });
      toast.success("Job moved to applications successfully!");
    } catch (error) {
      console.error('Failed to move job to applications:', error);
      toast.error("Failed to move job to applications. Please try again.");
    }
  };

  // Handler for removing job from matches
  const handleNotInterested = (jobMatch: JobMatch) => {
    setSelectedJobMatch(jobMatch);
    setShowNotInterestedDialog(true);
  };

  // Handler for confirming not interested action
  const handleConfirmNotInterested = async () => {
    if (!selectedJobMatch) return;
    
    try {
      await deleteJobMatch(selectedJobMatch.id);
      // Invalidate and refetch job matches
      queryClient.invalidateQueries({ queryKey: ["jobMatches"] });
      queryClient.invalidateQueries({ queryKey: ["jobMatchStats"] });
      toast.success("Job removed successfully. It won't be shown again.");
    } catch (error) {
      console.error('Failed to remove job:', error);
      toast.error("Failed to remove job. Please try again.");
    } finally {
      setShowNotInterestedDialog(false);
      setSelectedJobMatch(null);
    }
  };

  // Show all job matches - filtering by status is now handled by the backend
  const filteredJobMatches = jobMatches;

  return (
    <div className="space-y-4">
      {error && (
        <Card className="border-red-200 dark:border-red-800">
          <CardContent className="p-6 text-center">
            <p className="text-red-600 dark:text-red-400">
              Failed to load job matches. Please try again later.
            </p>
          </CardContent>
        </Card>
      )}
      
      {!error && filteredJobMatches.length === 0 ? (
        <div className="text-center py-8">
          <div className="mx-auto w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4">
            <Bookmark className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            No job matches yet
          </h3>
          <p className="text-gray-500 dark:text-gray-400 mb-4">
            Complete your profile and set job preferences to get personalized job matches.
          </p>
          <Button className="inline-flex items-center">
            <Plus className="mr-2 h-4 w-4" />
            Complete Profile
          </Button>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex justify-between items-center mb-4">
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Found {filteredJobMatches.length} matching jobs
            </p>
          </div>
          
          {filteredJobMatches.map((match) => (
            <Card key={match.id} className="hover:shadow-md transition-shadow duration-200 border-0 bg-gray-50 dark:bg-slate-800/50">
              <CardContent className="p-4">
                <div className="flex justify-between items-start mb-3">
                  <div className="flex-1">
                    <h3 className="font-semibold text-base text-gray-900 dark:text-white mb-1">
                      {match.job.job_title || 'Job Title Not Available'}
                    </h3>
                    <div className="flex items-center text-gray-600 dark:text-gray-300 mb-2">
                      <Building className="mr-1 h-4 w-4" />
                      <span className="text-sm">{match.job.employer_name || 'Company Not Available'}</span>
                    </div>
                  </div>
                  <div className="flex flex-col items-end space-y-1">
                    <div className={`font-bold text-base ${getRelevanceColor(match.relevance_score)}`}>
                      {formatRelevanceScore(match.relevance_score)}
                    </div>
                    <Badge variant="secondary" className="text-xs">
                      Match Score
                    </Badge>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
                  <div className="space-y-1">
                    {match.job.job_city && (
                      <div className="flex items-center text-gray-600 dark:text-gray-300 text-sm">
                        <MapPin className="mr-1 h-3 w-3" />
                        <span>
                          {match.job.job_city}
                          {match.job.job_country && `, ${match.job.job_country}`}
                          {match.job.job_is_remote && ' (Remote)'}
                        </span>
                      </div>
                    )}
                    
                    {match.job.job_employment_type && (
                      <div className="flex items-center">
                        <Clock className="mr-1 h-3 w-3 text-gray-400" />
                        <Badge className={`text-xs ${getEmploymentTypeColor(match.job.job_employment_type)}`}>
                          {match.job.job_employment_type}
                        </Badge>
                      </div>
                    )}
                  </div>
                  
                  <div className="space-y-1">
                    {match.job.job_posted_at_datetime_utc && (
                      <div className="flex items-center text-gray-600 dark:text-gray-300 text-sm">
                        <Calendar className="mr-1 h-3 w-3" />
                        <span>Posted {formatJobPostedDate(match.job.job_posted_at_datetime_utc)}</span>
                      </div>
                    )}
                    
                    {(match.job.job_min_salary || match.job.job_max_salary) && (
                      <div className="text-sm text-gray-600 dark:text-gray-300">
                        <span className="font-medium">Salary: </span>
                        {match.job.job_min_salary && match.job.job_max_salary
                          ? `${match.job.job_salary_currency || ''}${match.job.job_min_salary} - ${match.job.job_max_salary}`
                          : match.job.job_min_salary
                          ? `${match.job.job_salary_currency || ''}${match.job.job_min_salary}+`
                          : `Up to ${match.job.job_salary_currency || ''}${match.job.job_max_salary}`}
                        {match.job.job_salary_period && ` per ${match.job.job_salary_period}`}
                      </div>
                    )}
                  </div>
                </div>
                
                {match.job.job_description && (
                  <div className="mb-3">
                    <p className="text-sm text-gray-600 dark:text-gray-300 overflow-hidden" style={{
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical'
                    }}>
                      {match.job.job_description.substring(0, 150)}
                      {match.job.job_description.length > 150 && '...'}
                    </p>
                  </div>
                )}
                
                <div className="flex flex-wrap gap-2 justify-between items-center">
                  {match.status === 'applied' ? (
                    <Button 
                      variant="outline" 
                      size="sm"
                      disabled
                      className="text-green-600 dark:text-green-400 border-green-300 dark:border-green-600 bg-green-50 dark:bg-green-900/20"
                    >
                      <CheckCircle className="mr-1 h-3 w-3" />
                      Applied
                    </Button>
                  ) : (
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => handleMoveToApplications(match)}
                      className="text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20"
                    >
                      <Check className="mr-1 h-3 w-3" />
                      Add to Applications
                    </Button>
                  )}
                  
                  <div className="flex gap-2">
                    {match.status !== 'applied' && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleNotInterested(match)}
                        className="text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
                      >
                        <X className="mr-1 h-3 w-3" />
                        Not Interested
                      </Button>
                    )}
                    <Button
                      size="sm"
                      onClick={() => handleApplyClick(match.job.job_apply_link)}
                      disabled={!match.job.job_apply_link}
                      className="bg-blue-600 hover:bg-blue-700 text-white"
                    >
                      <ExternalLink className="mr-1 h-3 w-3" />
                      Apply Now
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Not Interested Confirmation Dialog */}
      <Dialog open={showNotInterestedDialog} onOpenChange={setShowNotInterestedDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Remove Job Match</DialogTitle>
            <DialogDescription>
              This job won't be shown again. Are you sure you want to mark this job as not interested?
            </DialogDescription>
          </DialogHeader>
          {selectedJobMatch && (
            <div className="py-4">
              <p className="font-medium">{selectedJobMatch.job.job_title}</p>
              <p className="text-sm text-gray-600">{selectedJobMatch.job.employer_name}</p>
            </div>
          )}
          <DialogFooter>
            <Button 
              variant="outline" 
              onClick={() => setShowNotInterestedDialog(false)}
            >
              Cancel
            </Button>
            <Button 
              variant="destructive" 
              onClick={handleConfirmNotInterested}
            >
              Confirm Not Interested
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default JobMatchesList;
