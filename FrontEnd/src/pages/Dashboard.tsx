
import React from 'react';
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchProfile, fetchCompleteProfile, fetchDashboardData } from "@/lib/api";
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from "@/components/ui/card";
import { 
  Briefcase, 
  FileText, 
  Settings,
  User,
  MessageSquare,
  MapPin,
  Mail,
  Phone,
  Calendar,
  Building,
  Clock,
  Users,
  Award,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  XCircle,
  Edit,
  Upload,
  Search,
  Target,
  RefreshCw
} from "lucide-react";
import Navbar from '@/components/Navbar';
import DashboardStats from '@/components/dashboard/DashboardStats';
import JobMatchesList from '@/components/dashboard/JobMatchesList';
import ApplicationsList from '@/components/dashboard/ApplicationsList';
import ProfileIncompleteModal from '@/components/ProfileIncompleteModal';
import { useAuth } from "@/contexts/AuthContext";
import { JobProvider } from "@/contexts/JobContext";

const Dashboard = () => {
  const [activeTab, setActiveTab] = React.useState("matches");
  const [portfolioTab, setPortfolioTab] = React.useState("profile");
  const [showProfileModal, setShowProfileModal] = React.useState(false);
  const { token } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const queryClient = useQueryClient();
  
  React.useEffect(() => {
    if (!token) {
      navigate("/signin");
    }
  }, [token, navigate]);

  // Fetch dashboard data with auto job search logic
  const { data: dashboardResponse, isLoading: dashboardLoading, error: dashboardError } = useQuery({
    queryKey: ["dashboard"],
    queryFn: fetchDashboardData,
    enabled: !!token,
    retry: 2, // Retry failed requests up to 2 times
  });

  const dashboardData = dashboardResponse?.data;

  // Handle dashboard error
  React.useEffect(() => {
    if (dashboardError && !dashboardLoading) {
      console.error("Dashboard API error:", dashboardError);
      // Only show toast if it's not a network/auth error that would redirect
      if ((dashboardError as any)?.response?.status !== 401 && (dashboardError as any)?.response?.status !== 403) {
        toast.error("Unable to load dashboard. Please refresh the page.");
      }
    }
  }, [dashboardError, dashboardLoading]);

  // Fetch the user's profile with enhanced user information
  const { 
    data: profileResponse, 
    error: profileError, 
    refetch: refetchProfile,
    isRefetching 
  } = useQuery({
    queryKey: ["completeProfile"],
    queryFn: fetchCompleteProfile,
    enabled: !!token,
    refetchOnWindowFocus: true,  // Refetch when user returns to tab
    staleTime: 30000,            // Consider data stale after 30 seconds
  });
  
  const profile = profileResponse?.data;

  // Handle dashboard data changes
  React.useEffect(() => {
    if (!dashboardData) return;

    if (dashboardData.status === "incomplete_profile") {
      setShowProfileModal(true);
    }
  }, [dashboardData]);

  // Refresh profile data when navigating to dashboard
  React.useEffect(() => {
    if (location.pathname === '/dashboard') {
      // Small delay to ensure navigation is complete
      setTimeout(() => {
        queryClient.invalidateQueries({ queryKey: ["completeProfile"] });
      }, 100);
    }
  }, [location.pathname, queryClient]);

  // Handle profile error with retry option
  React.useEffect(() => {
    if (profileError) {
      console.error("Profile fetch error:", profileError);
      toast.error("Failed to load profile data. Please refresh.", {
        action: {
          label: "Retry",
          onClick: () => refetchProfile()
        }
      });
    }
  }, [profileError, refetchProfile]);

  // Function to refresh profile data
  const refreshProfileData = async () => {
    try {
      await refetchProfile();
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      toast.success("Profile data refreshed!");
    } catch (error) {
      toast.error("Failed to refresh profile data");
    }
  };

  // Get job statistics from dashboard data or defaults
  const getJobStats = () => {
    if (dashboardData?.dashboard_stats) {
      return dashboardData.dashboard_stats;
    }
    return {
      total_matches: 0,
      high_relevance_jobs: 0,
      recent_matches: 0,
      applied_jobs: 0
    };
  };

  const jobStats = getJobStats();
  const totalMatches = jobStats.total_matches || 0;
  const highRelevanceJobs = jobStats.high_relevance_jobs || 0;
  const recentMatches = jobStats.recent_matches || 0;
  const appliedJobs = jobStats.applied_jobs || 0;

  // Profile Section Component
  const ProfileSection = () => (
    <div className="space-y-6 relative">
      {/* Floating Update Profile Button */}
      <Button 
        onClick={() => navigate('/job-preferences')} 
        className="absolute top-0 right-4 z-10 shadow-lg"
        size="sm"
      >
        <Edit className="mr-2 h-4 w-4" />
        Update Profile
      </Button>
      
      <div className="pt-12">
        <Card className="border-0 shadow-sm">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center text-lg font-semibold">
              <User className="mr-2 h-5 w-5 text-blue-600" />
              Personal Information
            </CardTitle>
          </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center space-x-3">
              <User className="h-4 w-4 text-gray-500" />
              <div>
                <p className="text-sm text-gray-500">Name</p>
                <p className="font-medium">
                  {profile?.user_name 
                    ? profile.user_name.charAt(0).toUpperCase() + profile.user_name.slice(1).toLowerCase()
                    : 'Not provided'
                  }
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Mail className="h-4 w-4 text-gray-500" />
              <div>
                <p className="text-sm text-gray-500">Email</p>
                <p className="font-medium">{profile?.user_email || 'Not provided'}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Calendar className="h-4 w-4 text-gray-500" />
              <div>
                <p className="text-sm text-gray-500">Last Updated</p>
                <p className="font-medium">
                  {profile?.last_updated ? new Date(profile.last_updated).toLocaleDateString() : 'Not available'}
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="border-0 shadow-sm">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center text-lg font-semibold">
            <Settings className="mr-2 h-5 w-5 text-green-600" />
            Job Preferences
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-3">
              <div>
                <p className="text-sm text-gray-500">Job Title/Query</p>
                <p className="font-medium">{profile?.query || 'Not set'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Location</p>
                <p className="font-medium flex items-center">
                  <MapPin className="h-4 w-4 mr-1 text-gray-400" />
                  {profile?.location || 'Not set'}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Work Mode</p>
                <p className="font-medium">{profile?.mode_of_job || 'Not set'}</p>
              </div>
            </div>
            <div className="space-y-3">
              <div>
                <p className="text-sm text-gray-500">Experience Level</p>
                <p className="font-medium">{profile?.work_experience || 'Not set'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Employment Types</p>
                <div className="flex flex-wrap gap-1">
                  {profile?.employment_types?.length > 0 ? (
                    profile.employment_types.map((type: string, index: number) => (
                      <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-md">
                        {type}
                      </span>
                    ))
                  ) : (
                    <p className="font-medium">Not set</p>
                  )}
                </div>
              </div>
              <div>
                <p className="text-sm text-gray-500">Company Types</p>
                <div className="flex flex-wrap gap-1">
                  {profile?.company_types?.length > 0 ? (
                    profile.company_types.map((type: string, index: number) => (
                      <span key={index} className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-md">
                        {type}
                      </span>
                    ))
                  ) : (
                    <p className="font-medium">Not set</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
      </div>
    </div>
  );

  // Resume Section Component
  const ResumeSection = () => (
    <div className="space-y-6 relative">
      {/* Floating Update Resume Button */}
      <Button 
        onClick={() => navigate('/resume-upload')} 
        className="absolute top-0 right-4 z-10 shadow-lg"
        size="sm"
      >
        <FileText className="mr-2 h-4 w-4" />
        Update Resume
      </Button>
      
      <div className="pt-12">
        {profile?.resume_parsed ? (
        <>
          {/* Personal Info */}
          {profile.resume_parsed.personal_info && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold">
                  <User className="mr-2 h-5 w-5 text-blue-600" />
                  Personal Information
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(profile.resume_parsed.personal_info).map(([key, value]) => 
                    value && (
                      <div key={key} className="space-y-1">
                        <p className="text-sm text-gray-500 capitalize">{key.replace('_', ' ')}</p>
                        <p className="font-medium">{value as string}</p>
                      </div>
                    )
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Professional Summary */}
          {profile.resume_parsed.summary && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold">
                  <FileText className="mr-2 h-5 w-5 text-indigo-600" />
                  Professional Summary
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 leading-relaxed">{profile.resume_parsed.summary}</p>
              </CardContent>
            </Card>
          )}

          {/* Experience */}
          {profile.resume_parsed.experience?.length > 0 && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold">
                  <Briefcase className="mr-2 h-5 w-5 text-green-600" />
                  Work Experience
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {profile.resume_parsed.experience.map((exp: any, index: number) => (
                  <div key={index} className="relative pl-6 border-l-2 border-blue-200 last:border-l-0">
                    <div className="absolute -left-2 top-0 w-4 h-4 bg-blue-500 rounded-full"></div>
                    <div className="space-y-2">
                      <h4 className="font-semibold text-lg">{exp.role}</h4>
                      <p className="text-gray-600 font-medium">{exp.company}</p>
                      <div className="flex flex-wrap gap-4 text-sm text-gray-500">
                        <span className="flex items-center">
                          <Calendar className="h-4 w-4 mr-1" />
                          {exp.dates}
                        </span>
                        {exp.location && (
                          <span className="flex items-center">
                            <MapPin className="h-4 w-4 mr-1" />
                            {exp.location}
                          </span>
                        )}
                      </div>
                      {exp.description && exp.description.length > 0 && (
                        <ul className="mt-3 space-y-1">
                          {exp.description.map((desc: string, i: number) => (
                            <li key={i} className="text-gray-600 flex items-start">
                              <span className="text-blue-500 mr-2 mt-1.5">•</span>
                              <span>{desc}</span>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          {/* Education */}
          {profile.resume_parsed.education?.length > 0 && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold">
                  <Building className="mr-2 h-5 w-5 text-orange-600" />
                  Education
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {profile.resume_parsed.education.map((edu: any, index: number) => (
                  <div key={index} className="border-l-2 border-orange-200 pl-4">
                    <h4 className="font-semibold text-lg">{edu.degree}</h4>
                    <p className="text-gray-600 font-medium">{edu.institution}</p>
                    <div className="flex flex-wrap gap-4 text-sm text-gray-500 mt-1">
                      {edu.dates && (
                        <span className="flex items-center">
                          <Calendar className="h-4 w-4 mr-1" />
                          {edu.dates}
                        </span>
                      )}
                      {edu.location && (
                        <span className="flex items-center">
                          <MapPin className="h-4 w-4 mr-1" />
                          {edu.location}
                        </span>
                      )}
                      {edu.gpa && (
                        <span className="flex items-center">
                          <Award className="h-4 w-4 mr-1" />
                          GPA: {edu.gpa}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          {/* Skills */}
          {profile.resume_parsed.skills?.length > 0 && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold">
                  <Award className="mr-2 h-5 w-5 text-purple-600" />
                  Technical Skills
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {profile.resume_parsed.skills.map((skill: string, index: number) => (
                    <span key={index} className="px-3 py-2 bg-gradient-to-r from-purple-100 to-pink-100 text-purple-800 text-sm rounded-full font-medium hover:from-purple-200 hover:to-pink-200 transition-all duration-200">
                      {skill}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Projects */}
          {profile.resume_parsed.projects?.length > 0 && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold">
                  <Settings className="mr-2 h-5 w-5 text-cyan-600" />
                  Projects
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {profile.resume_parsed.projects.map((project: any, index: number) => (
                  <div key={index} className="border rounded-lg p-4 bg-gray-50">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-lg">{project.name}</h4>
                      {project.link && (
                        <a 
                          href={project.link} 
                          target="_blank" 
                          rel="noopener noreferrer" 
                          className="text-blue-600 hover:text-blue-800 text-sm"
                        >
                          View Project →
                        </a>
                      )}
                    </div>
                    {project.dates && (
                      <p className="text-sm text-gray-500 mb-2">{project.dates}</p>
                    )}
                    {project.description && (
                      <p className="text-gray-700 mb-3">{project.description}</p>
                    )}
                    {project.technologies?.length > 0 && (
                      <div className="space-y-1">
                        <p className="text-sm font-medium text-gray-600">Technologies Used:</p>
                        <div className="flex flex-wrap gap-1">
                          {project.technologies.map((tech: string, i: number) => (
                            <span key={i} className="px-2 py-1 bg-cyan-100 text-cyan-800 text-xs rounded-md">
                              {tech}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          {/* Certifications */}
          {profile.resume_parsed.certifications?.length > 0 && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold">
                  <Award className="mr-2 h-5 w-5 text-yellow-600" />
                  Certifications
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {profile.resume_parsed.certifications.map((cert: string, index: number) => (
                    <div key={index} className="flex items-center p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <Award className="h-4 w-4 text-yellow-600 mr-2 flex-shrink-0" />
                      <span className="text-gray-800 font-medium">{cert}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Courses Undertaken */}
          {profile.resume_parsed.courses_undertaken?.length > 0 && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold">
                  <Building className="mr-2 h-5 w-5 text-teal-600" />
                  Courses & Training
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {profile.resume_parsed.courses_undertaken.map((course: string, index: number) => (
                    <div key={index} className="p-2 bg-teal-50 border border-teal-200 rounded text-sm">
                      <span className="text-teal-800">{course}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Achievements */}
          {profile.resume_parsed.achievements?.length > 0 && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold">
                  <TrendingUp className="mr-2 h-5 w-5 text-emerald-600" />
                  Achievements & Awards
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {profile.resume_parsed.achievements.map((achievement: string, index: number) => (
                    <li key={index} className="flex items-start">
                      <TrendingUp className="h-4 w-4 text-emerald-500 mt-1 mr-2 flex-shrink-0" />
                      <span className="text-gray-700">{achievement}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}
        </>
      ) : (
        <Card className="border-0 shadow-sm">
          <CardContent className="text-center py-12">
            <FileText className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Resume Uploaded</h3>
            <p className="text-gray-500 mb-4">Upload your resume to see parsed information here.</p>
            <Button onClick={() => navigate('/resume-upload')}>
              Upload Resume
            </Button>
          </CardContent>
        </Card>
      )}
      </div>
    </div>
  );

  // Remarks Section Component
  const RemarksSection = () => (
    <div className="space-y-6">
      {profile?.resume_remarks ? (
        <>
          {/* Good Points */}
          {profile.resume_remarks.good_points?.length > 0 && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold text-green-700">
                  <CheckCircle className="mr-2 h-5 w-5" />
                  Strengths
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {profile.resume_remarks.good_points.map((point: string, index: number) => (
                    <li key={index} className="flex items-start">
                      <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 mr-2 flex-shrink-0" />
                      <span className="text-gray-700">{point}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {/* Weak Points */}
          {profile.resume_remarks.weak_points?.length > 0 && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold text-orange-700">
                  <AlertCircle className="mr-2 h-5 w-5" />
                  Areas for Improvement
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {profile.resume_remarks.weak_points.map((point: string, index: number) => (
                    <li key={index} className="flex items-start">
                      <AlertCircle className="h-4 w-4 text-orange-500 mt-0.5 mr-2 flex-shrink-0" />
                      <span className="text-gray-700">{point}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {/* Missing Things */}
          {profile.resume_remarks.missing_things?.length > 0 && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold text-red-700">
                  <XCircle className="mr-2 h-5 w-5" />
                  Missing Elements
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {profile.resume_remarks.missing_things.map((point: string, index: number) => (
                    <li key={index} className="flex items-start">
                      <XCircle className="h-4 w-4 text-red-500 mt-0.5 mr-2 flex-shrink-0" />
                      <span className="text-gray-700">{point}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {/* Improvements */}
          {profile.resume_remarks.improvements?.length > 0 && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold text-blue-700">
                  <TrendingUp className="mr-2 h-5 w-5" />
                  Suggestions for Improvement
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {profile.resume_remarks.improvements.map((point: string, index: number) => (
                    <li key={index} className="flex items-start">
                      <TrendingUp className="h-4 w-4 text-blue-500 mt-0.5 mr-2 flex-shrink-0" />
                      <span className="text-gray-700">{point}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {/* Redundancy */}
          {profile.resume_remarks.redundancy?.length > 0 && (
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center text-lg font-semibold text-gray-700">
                  <AlertCircle className="mr-2 h-5 w-5" />
                  Redundant Content
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {profile.resume_remarks.redundancy.map((point: string, index: number) => (
                    <li key={index} className="flex items-start">
                      <AlertCircle className="h-4 w-4 text-gray-500 mt-0.5 mr-2 flex-shrink-0" />
                      <span className="text-gray-700">{point}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}
        </>
      ) : (
        <Card className="border-0 shadow-sm">
          <CardContent className="text-center py-12">
            <MessageSquare className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Analysis Available</h3>
            <p className="text-gray-500">Upload and parse your resume to see AI-powered analysis and recommendations.</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
  
  return (
    <JobProvider>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        
        <div className="flex-1 bg-gray-50 dark:bg-slate-900 pt-6 pb-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
                <p className="text-gray-600 dark:text-gray-300">Welcome back! Here's your job search overview.</p>
              </div>
            </div>
            
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {/* Profile Status Card */}
              <Card className="border-0 shadow-sm">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <User className="h-8 w-8 text-blue-600" />
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-500">Profile Status</p>
                        <p className="text-xl font-semibold text-gray-900">
                          {(() => {
                            // Fixed: Use correct field names from CompleteUserProfile schema
                            const hasResume = profile?.resume_parsed;  // This is the correct field
                            const hasPreferences = profile?.preferences_set;
                            
                            if (!hasResume && !hasPreferences) return 'Incomplete';
                            if (!hasResume) return 'No Resume Found';
                            if (!hasPreferences) return 'Preferences Not Set';
                            return 'Complete';
                          })()}
                        </p>
                      </div>
                    </div>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      onClick={refreshProfileData}
                      disabled={isRefetching}
                      className="ml-2"
                    >
                      <RefreshCw className={`h-4 w-4 ${isRefetching ? 'animate-spin' : ''}`} />
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* Job Matches Card - Replaces Resume card */}
              <Card className="border-0 shadow-sm">
                <CardContent className="p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <Search className="h-8 w-8 text-green-600" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Jobs Matched</p>
                      <p className="text-xl font-semibold text-gray-900">
                        {totalMatches}
                      </p>
                      <p className="text-xs text-gray-500">
                        <span className="text-blue-500">{recentMatches}</span> new matches today
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* High Relevance Jobs Card - Replaces AI Analysis card */}
              <Card className="border-0 shadow-sm">
                <CardContent className="p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <Target className="h-8 w-8 text-purple-600" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">High Relevance Jobs</p>
                      <p className="text-xl font-semibold text-gray-900">
                        {highRelevanceJobs}
                      </p>
                      <p className="text-xs text-gray-500">
                        70%+ match with your profile
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Applications Card - Replaces Job Matches card */}
              <Card className="border-0 shadow-sm">
                <CardContent className="p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <FileText className="h-8 w-8 text-orange-600" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-500">Applications</p>
                      <p className="text-xl font-semibold text-gray-900">
                        {appliedJobs}
                      </p>
                      <p className="text-xs text-gray-500">
                        <span className="text-green-500">0</span> from last week
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Main Content */}
            <div className="space-y-8">
              {/* Portfolio Section - Full Width */}
              <Card className="border-0 shadow-sm">
                <CardHeader className="pb-0">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-xl font-semibold">Portfolio</CardTitle>
                    <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
                      <Button
                        variant={portfolioTab === "profile" ? "default" : "ghost"}
                        size="sm"
                        onClick={() => setPortfolioTab("profile")}
                        className="text-xs"
                      >
                        <User className="h-3 w-3 mr-1" />
                        Profile
                      </Button>
                      <Button
                        variant={portfolioTab === "resume" ? "default" : "ghost"}
                        size="sm"
                        onClick={() => setPortfolioTab("resume")}
                        className="text-xs"
                      >
                        <FileText className="h-3 w-3 mr-1" />
                        Resume
                      </Button>
                      <Button
                        variant={portfolioTab === "remarks" ? "default" : "ghost"}
                        size="sm"
                        onClick={() => setPortfolioTab("remarks")}
                        className="text-xs"
                      >
                        <MessageSquare className="h-3 w-3 mr-1" />
                        Analysis
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="pt-6">
                  <div className="h-[28rem] overflow-y-auto">
                    {portfolioTab === "profile" && <ProfileSection />}
                    {portfolioTab === "resume" && <ResumeSection />}
                    {portfolioTab === "remarks" && <RemarksSection />}
                  </div>
                </CardContent>
              </Card>

              {/* Job Management Section */}
              <Card className="border-0 shadow-sm">
                <CardHeader className="pb-0">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-xl font-semibold">Job Management</CardTitle>
                    <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
                      <Button
                        variant={activeTab === "matches" ? "default" : "ghost"}
                        size="sm"
                        onClick={() => setActiveTab("matches")}
                        className="text-xs"
                      >
                        <Search className="h-3 w-3 mr-1" />
                        Job Matches
                      </Button>
                      <Button
                        variant={activeTab === "applications" ? "default" : "ghost"}
                        size="sm"
                        onClick={() => setActiveTab("applications")}
                        className="text-xs"
                      >
                        <FileText className="h-3 w-3 mr-1" />
                        Applications
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="pt-6">
                  <div className="h-[28rem] overflow-y-auto">
                    {activeTab === "matches" && <JobMatchesList />}
                    {activeTab === "applications" && <ApplicationsList />}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>

      {/* Profile Incomplete Modal */}
      <ProfileIncompleteModal
        isOpen={showProfileModal}
        onClose={() => setShowProfileModal(false)}
        needsResume={dashboardData?.needs_resume || false}
        needsPreferences={dashboardData?.needs_preferences || false}
      />
    </JobProvider>
  );
};

export default Dashboard;
