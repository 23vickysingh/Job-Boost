import React, { createContext, useContext, useState, ReactNode } from 'react';

// Job interface matching the API structure
export interface Job {
  id: number;
  job_id: string;
  employer_name?: string;
  job_title?: string;
  job_description?: string;
  job_apply_link?: string;
  job_city?: string;
  job_country?: string;
  job_employment_type?: string;
  employer_logo?: string;
  job_is_remote?: boolean;
  job_posted_at_datetime_utc?: string;
  job_required_skills?: string[];
  job_min_salary?: number;
  job_max_salary?: number;
  job_salary_currency?: string;
  job_salary_period?: string;
}

// JobMatch interface
export interface JobMatch {
  id: number;
  user_id: number;
  job_id: number;
  relevance_score: number;
  created_at: string;
  job: Job;
}

// Application interface
export interface Application {
  id: number;
  job_id: string;
  title: string;
  company: string;
  appliedDate: string;
  status: string;
  job: Job;
}

interface JobContextType {
  applications: Application[];
  appliedJobIds: Set<string>;
  removedJobIds: Set<number>;
  addToApplications: (jobMatch: JobMatch) => void;
  removeApplication: (applicationId: number) => void;
  removeJobMatch: (jobMatchId: number) => void;
  isJobApplied: (jobId: string) => boolean;
  isJobRemoved: (jobMatchId: number) => boolean;
}

const JobContext = createContext<JobContextType | undefined>(undefined);

export const useJobs = () => {
  const context = useContext(JobContext);
  if (!context) {
    throw new Error('useJobs must be used within a JobProvider');
  }
  return context;
};

interface JobProviderProps {
  children: ReactNode;
}

export const JobProvider: React.FC<JobProviderProps> = ({ children }) => {
  const [applications, setApplications] = useState<Application[]>([]);
  const [appliedJobIds, setAppliedJobIds] = useState<Set<string>>(new Set());
  const [removedJobIds, setRemovedJobIds] = useState<Set<number>>(new Set());

  const addToApplications = (jobMatch: JobMatch) => {
    const newApplication: Application = {
      id: Date.now(), // Generate unique ID
      job_id: jobMatch.job.job_id,
      title: jobMatch.job.job_title || 'Unknown Position',
      company: jobMatch.job.employer_name || 'Unknown Company',
      appliedDate: new Date().toLocaleDateString(),
      status: 'Applied',
      job: jobMatch.job,
    };

    setApplications(prev => [...prev, newApplication]);
    setAppliedJobIds(prev => new Set(prev.add(jobMatch.job.job_id)));
  };

  const removeApplication = (applicationId: number) => {
    setApplications(prev => prev.filter(app => app.id !== applicationId));
    // Find the application to get its job_id and remove from applied set
    const appToRemove = applications.find(app => app.id === applicationId);
    if (appToRemove) {
      setAppliedJobIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(appToRemove.job_id);
        return newSet;
      });
    }
  };

  const removeJobMatch = (jobMatchId: number) => {
    setRemovedJobIds(prev => new Set(prev.add(jobMatchId)));
  };

  const isJobApplied = (jobId: string) => {
    return appliedJobIds.has(jobId);
  };

  const isJobRemoved = (jobMatchId: number) => {
    return removedJobIds.has(jobMatchId);
  };

  return (
    <JobContext.Provider value={{
      applications,
      appliedJobIds,
      removedJobIds,
      addToApplications,
      removeApplication,
      removeJobMatch,
      isJobApplied,
      isJobRemoved,
    }}>
      {children}
    </JobContext.Provider>
  );
};
