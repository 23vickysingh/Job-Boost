
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  Edit, 
  Mail, 
  Phone, 
  MapPin, 
  User, 
  Briefcase, 
  Clock, 
  Building, 
  GraduationCap,
  Award,
  FileText,
  Calendar,
  Link as LinkIcon,
  Code,
  DollarSign
} from 'lucide-react'; 
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface Profile {
  id?: number;
  user_id?: number;
  user_email?: string;
  user_name?: string;
  query?: string;
  location?: string;
  mode_of_job?: string;
  work_experience?: string;
  employment_types?: string[];
  company_types?: string[];
  job_requirements?: string;
  resume_location?: string;
  resume_parsed?: {
    parsed_data?: {
      personal_info?: {
        name?: string;
        email?: string;
        phone?: string;
        linkedin?: string;
        github?: string;
        location?: string;
      };
      summary?: string;
      experience?: Array<{
        role?: string;
        company?: string;
        dates?: string;
        location?: string;
        description?: string[];
      }>;
      education?: Array<{
        degree?: string;
        institution?: string;
        dates?: string;
        gpa?: string;
        location?: string;
      }>;
      skills?: string[];
      projects?: Array<{
        name?: string;
        technologies?: string[];
        description?: string;
        dates?: string;
        link?: string;
      }>;
      courses_undertaken?: string[];
      achievements?: string[];
      certifications?: string[];
    };
    // Direct structure (fallback)
    personal_info?: {
      name?: string;
      email?: string;
      phone?: string;
      linkedin?: string;
      github?: string;
      location?: string;
    };
    summary?: string;
    experience?: Array<{
      role?: string;
      company?: string;
      dates?: string;
      location?: string;
      description?: string[];
    }>;
    education?: Array<{
      degree?: string;
      institution?: string;
      dates?: string;
      gpa?: string;
      location?: string;
    }>;
    skills?: string[];
    projects?: Array<{
      name?: string;
      technologies?: string[];
      description?: string;
      dates?: string;
      link?: string;
    }>;
    courses_undertaken?: string[];
    achievements?: string[];
    certifications?: string[];
  };
  last_updated?: string;
}

interface UserProfileProps {
  onEditClick: () => void;
  profile?: Profile;
}

const UserProfile: React.FC<UserProfileProps> = ({ onEditClick, profile }) => {
  // Debug logging to see the actual data structure
  React.useEffect(() => {
    if (profile) {
      console.log("Profile data received:", profile);
      console.log("Resume parsed structure:", profile.resume_parsed);
      if (profile.resume_parsed?.parsed_data) {
        console.log("Parsed data found:", profile.resume_parsed.parsed_data);
      }
    }
  }, [profile]);

  // Extract resume data - check both direct structure and parsed_data structure
  const resumeData = profile?.resume_parsed?.parsed_data || profile?.resume_parsed;
  const personalInfo = resumeData?.personal_info;
  
  // Prioritize parsed resume data for name and email, fallback to profile data
  const userName = profile?.user_name || personalInfo?.name || "Name not available";
  const userEmail = personalInfo?.email || profile?.user_email || "Email not available";
  
  const jobPrefs = {
    query: profile?.query,
    location: profile?.location,
    mode: profile?.mode_of_job,
    experience: profile?.work_experience,
    employmentTypes: profile?.employment_types || [],
    companyTypes: profile?.company_types || [],
    requirements: profile?.job_requirements
  };

  const hasJobPreferences = jobPrefs.query || jobPrefs.location || jobPrefs.mode;
  const hasResumeData = resumeData && Object.keys(resumeData).length > 0;

  return (
    <div className="space-y-6 mb-6">
      {/* Main Profile Section */}
      <Card className="overflow-hidden">
        <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
          <div className="flex flex-col sm:flex-row items-center justify-between">
            <CardTitle className="text-xl font-semibold flex items-center">
              <User className="mr-2 h-5 w-5" />
              Profile Overview
            </CardTitle>
            <Button 
              variant="outline" 
              size="sm" 
              onClick={onEditClick} 
              className="flex items-center gap-2 bg-white text-gray-800 hover:bg-gray-100 mt-4 sm:mt-0"
            >
              <Edit className="h-4 w-4" />
              Update Profile
            </Button>
          </div>
        </CardHeader>
        <CardContent className="p-6">
          <div className="grid md:grid-cols-2 gap-6">
            {/* Basic Info */}
            <div className="flex flex-col sm:flex-row gap-4 items-center sm:items-start">
              <Avatar className="h-20 w-20 ring-4 ring-blue-100">
                <AvatarImage src="https://github.com/shadcn.png" alt={userName} />
                <AvatarFallback className="text-lg bg-blue-500 text-white">
                  {userName !== "Name not available" ? 
                    userName.split(' ').map((n: string) => n[0]).join('').toUpperCase() :
                    "U"
                  }
                </AvatarFallback>
              </Avatar>

              <div className="text-center sm:text-left">
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                  {userName}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 flex items-center justify-center sm:justify-start mt-1">
                  <Mail className="h-4 w-4 mr-1" />
                  {userEmail}
                </p>
                {personalInfo?.location && (
                  <p className="text-sm text-gray-600 dark:text-gray-400 flex items-center justify-center sm:justify-start mt-1">
                    <MapPin className="h-4 w-4 mr-1" />
                    {personalInfo.location}
                  </p>
                )}
              </div>
            </div>

            {/* Contact Info */}
            <div className="space-y-3">
              {personalInfo?.phone && (
                <div className="flex items-center gap-2">
                  <Phone className="h-5 w-5 text-gray-500" />
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Phone</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{personalInfo.phone}</p>
                  </div>
                </div>
              )}

              {personalInfo?.linkedin && (
                <div className="flex items-center gap-2">
                  <LinkIcon className="h-5 w-5 text-gray-500" />
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">LinkedIn</p>
                    <a 
                      href={personalInfo.linkedin} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-sm text-blue-600 hover:underline"
                    >
                      {personalInfo.linkedin}
                    </a>
                  </div>
                </div>
              )}

              {personalInfo?.github && (
                <div className="flex items-center gap-2">
                  <Code className="h-5 w-5 text-gray-500" />
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">GitHub</p>
                    <a 
                      href={personalInfo.github} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-sm text-blue-600 hover:underline"
                    >
                      {personalInfo.github}
                    </a>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Summary */}
          {resumeData?.summary && (
            <div className="mt-6 p-4 bg-gray-50 dark:bg-slate-800 rounded-lg">
              <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Professional Summary</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
                {resumeData.summary}
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Job Preferences Section */}
      {hasJobPreferences && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold flex items-center">
              <Briefcase className="mr-2 h-5 w-5 text-blue-500" />
              Job Preferences
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              {jobPrefs.query && (
                <div className="flex items-center gap-2">
                  <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                    <Briefcase className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Job Title</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{jobPrefs.query}</p>
                  </div>
                </div>
              )}

              {jobPrefs.location && (
                <div className="flex items-center gap-2">
                  <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
                    <MapPin className="h-4 w-4 text-green-600 dark:text-green-400" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Preferred Location</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{jobPrefs.location}</p>
                  </div>
                </div>
              )}

              {jobPrefs.mode && (
                <div className="flex items-center gap-2">
                  <div className="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
                    <Clock className="h-4 w-4 text-purple-600 dark:text-purple-400" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Work Mode</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400 capitalize">{jobPrefs.mode}</p>
                  </div>
                </div>
              )}

              {jobPrefs.experience && (
                <div className="flex items-center gap-2">
                  <div className="p-2 bg-orange-100 dark:bg-orange-900 rounded-lg">
                    <Award className="h-4 w-4 text-orange-600 dark:text-orange-400" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Experience Level</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{jobPrefs.experience}</p>
                  </div>
                </div>
              )}
            </div>

            {/* Employment Types */}
            {jobPrefs.employmentTypes.length > 0 && (
              <div>
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Employment Types</p>
                <div className="flex flex-wrap gap-2">
                  {jobPrefs.employmentTypes.map((type, index) => (
                    <Badge key={index} variant="secondary" className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                      {type}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Company Types */}
            {jobPrefs.companyTypes.length > 0 && (
              <div>
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Preferred Company Types</p>
                <div className="flex flex-wrap gap-2">
                  {jobPrefs.companyTypes.map((type, index) => (
                    <Badge key={index} variant="secondary" className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                      {type}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Requirements */}
            {jobPrefs.requirements && (
              <div>
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Additional Requirements</p>
                <p className="text-sm text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-slate-800 p-3 rounded-lg">
                  {jobPrefs.requirements}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Enhanced Resume Information Section */}
      {hasResumeData && (
        <Card className="overflow-hidden relative">
          <CardHeader className="bg-gradient-to-r from-green-500 to-blue-600 text-white">
            <CardTitle className="text-lg font-semibold flex items-center">
              <FileText className="mr-2 h-5 w-5" />
              Resume Information
            </CardTitle>
            <p className="text-green-100 text-sm mt-1">
              Comprehensive overview of your professional background (scroll to view all sections)
            </p>
          </CardHeader>
          <CardContent className="h-96 overflow-y-auto p-6 space-y-8 scroll-smooth relative">
            <div className="space-y-8">
            
            {/* Professional Summary */}
            {resumeData?.summary && (
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl p-6 border border-blue-200 dark:border-blue-800">
                <h4 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-3 flex items-center">
                  <User className="mr-2 h-5 w-5 text-blue-600" />
                  Professional Summary
                </h4>
                <p className="text-gray-700 dark:text-gray-300 leading-relaxed italic">
                  "{resumeData.summary}"
                </p>
              </div>
            )}

            {/* Skills Section with Categories */}
            {resumeData?.skills && resumeData.skills.length > 0 && (
              <div className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
                <div className="bg-gradient-to-r from-purple-500 to-pink-500 px-6 py-4">
                  <h4 className="text-lg font-semibold text-white flex items-center">
                    <Code className="mr-2 h-5 w-5" />
                    Technical Skills & Expertise
                  </h4>
                </div>
                <div className="p-6">
                  <div className="flex flex-wrap gap-3">
                    {resumeData.skills.map((skill, index) => (
                      <Badge 
                        key={index} 
                        className="px-4 py-2 text-sm font-medium bg-gradient-to-r from-purple-100 to-pink-100 text-purple-800 border-purple-200 hover:from-purple-200 hover:to-pink-200 transition-all duration-200 transform hover:scale-105 dark:from-purple-900 dark:to-pink-900 dark:text-purple-200 dark:border-purple-700"
                      >
                        <Code className="mr-1 h-3 w-3" />
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Experience Timeline */}
            {resumeData?.experience && resumeData.experience.length > 0 && (
              <div className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
                <div className="bg-gradient-to-r from-orange-500 to-red-500 px-6 py-4">
                  <h4 className="text-lg font-semibold text-white flex items-center">
                    <Briefcase className="mr-2 h-5 w-5" />
                    Professional Experience
                  </h4>
                </div>
                <div className="p-6">
                  <div className="space-y-6">
                    {resumeData.experience.map((exp, index) => (
                      <div key={index} className="relative">
                        {/* Timeline line */}
                        {index !== resumeData.experience.length - 1 && (
                          <div className="absolute left-6 top-16 w-0.5 h-16 bg-gradient-to-b from-orange-300 to-red-300"></div>
                        )}
                        
                        <div className="flex items-start space-x-4">
                          <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center">
                            <Briefcase className="h-6 w-6 text-white" />
                          </div>
                          
                          <div className="flex-grow bg-gradient-to-r from-orange-50 to-red-50 dark:from-orange-900/20 dark:to-red-900/20 rounded-lg p-4 border border-orange-200 dark:border-orange-800">
                            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-3">
                              <h5 className="text-lg font-semibold text-gray-900 dark:text-white">{exp.role}</h5>
                              <span className="text-sm text-orange-600 dark:text-orange-400 font-medium flex items-center bg-orange-100 dark:bg-orange-900/30 px-3 py-1 rounded-full">
                                <Calendar className="mr-1 h-3 w-3" />
                                {exp.dates}
                              </span>
                            </div>
                            
                            <div className="flex flex-wrap items-center text-sm text-gray-600 dark:text-gray-400 mb-3 space-x-4">
                              <div className="flex items-center">
                                <Building className="mr-1 h-4 w-4 text-gray-500" />
                                <span className="font-medium">{exp.company}</span>
                              </div>
                              {exp.location && (
                                <div className="flex items-center">
                                  <MapPin className="mr-1 h-4 w-4 text-gray-500" />
                                  <span>{exp.location}</span>
                                </div>
                              )}
                            </div>
                            
                            {exp.description && exp.description.length > 0 && (
                              <div className="space-y-2">
                                <h6 className="text-sm font-medium text-gray-700 dark:text-gray-300">Key Responsibilities & Achievements:</h6>
                                <ul className="space-y-2">
                                  {exp.description.map((desc, descIndex) => (
                                    <li key={descIndex} className="flex items-start">
                                      <div className="w-2 h-2 bg-gradient-to-r from-orange-400 to-red-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                                      <span className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">{desc}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Education Section */}
            {resumeData?.education && resumeData.education.length > 0 && (
              <div className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
                <div className="bg-gradient-to-r from-teal-500 to-cyan-500 px-6 py-4">
                  <h4 className="text-lg font-semibold text-white flex items-center">
                    <GraduationCap className="mr-2 h-5 w-5" />
                    Educational Background
                  </h4>
                </div>
                <div className="p-6">
                  <div className="grid gap-4">
                    {resumeData.education.map((edu, index) => (
                      <div key={index} className="bg-gradient-to-r from-teal-50 to-cyan-50 dark:from-teal-900/20 dark:to-cyan-900/20 rounded-lg p-5 border border-teal-200 dark:border-teal-800 hover:shadow-lg transition-shadow duration-200">
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 bg-gradient-to-br from-teal-400 to-cyan-500 rounded-lg flex items-center justify-center">
                              <GraduationCap className="h-5 w-5 text-white" />
                            </div>
                            <div>
                              <h5 className="text-lg font-semibold text-gray-900 dark:text-white">{edu.degree}</h5>
                              <p className="text-teal-600 dark:text-teal-400 font-medium">{edu.institution}</p>
                            </div>
                          </div>
                          <span className="text-sm text-teal-600 dark:text-teal-400 font-medium bg-teal-100 dark:bg-teal-900/30 px-3 py-1 rounded-full">
                            {edu.dates}
                          </span>
                        </div>
                        
                        <div className="flex flex-wrap items-center text-sm text-gray-600 dark:text-gray-400 space-x-4">
                          {edu.location && (
                            <div className="flex items-center">
                              <MapPin className="mr-1 h-3 w-3" />
                              <span>{edu.location}</span>
                            </div>
                          )}
                          {edu.gpa && (
                            <div className="flex items-center">
                              <Award className="mr-1 h-3 w-3 text-yellow-500" />
                              <span className="font-medium">GPA: {edu.gpa}</span>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Projects Portfolio */}
            {resumeData?.projects && resumeData.projects.length > 0 && (
              <div className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
                <div className="bg-gradient-to-r from-indigo-500 to-purple-600 px-6 py-4">
                  <h4 className="text-lg font-semibold text-white flex items-center">
                    <Code className="mr-2 h-5 w-5" />
                    Project Portfolio
                  </h4>
                </div>
                <div className="p-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    {resumeData.projects.map((project, index) => (
                      <div key={index} className="bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 rounded-lg p-5 border border-indigo-200 dark:border-indigo-800 hover:shadow-lg transition-all duration-200 hover:scale-105">
                        <div className="flex items-center justify-between mb-3">
                          <div className="flex items-center space-x-2">
                            <div className="w-8 h-8 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-lg flex items-center justify-center">
                              <Code className="h-4 w-4 text-white" />
                            </div>
                            <h5 className="font-semibold text-gray-900 dark:text-white text-lg">{project.name}</h5>
                          </div>
                          {project.link && (
                            <a 
                              href={project.link} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="text-indigo-500 hover:text-indigo-700 bg-indigo-100 dark:bg-indigo-900/30 p-2 rounded-lg hover:bg-indigo-200 transition-colors duration-200"
                            >
                              <LinkIcon className="h-4 w-4" />
                            </a>
                          )}
                        </div>
                        
                        {project.dates && (
                          <p className="text-sm text-indigo-600 dark:text-indigo-400 mb-3 flex items-center font-medium">
                            <Calendar className="mr-1 h-3 w-3" />
                            {project.dates}
                          </p>
                        )}
                        
                        {project.description && (
                          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 leading-relaxed">{project.description}</p>
                        )}
                        
                        {project.technologies && project.technologies.length > 0 && (
                          <div>
                            <p className="text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">Technologies Used:</p>
                            <div className="flex flex-wrap gap-2">
                              {project.technologies.map((tech, techIndex) => (
                                <Badge 
                                  key={techIndex} 
                                  variant="secondary" 
                                  className="text-xs bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-800 border-indigo-200 dark:from-indigo-900 dark:to-purple-900 dark:text-indigo-200 dark:border-indigo-700"
                                >
                                  {tech}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Achievements & Recognition */}
            {resumeData?.achievements && resumeData.achievements.length > 0 && (
              <div className="bg-gradient-to-r from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 rounded-xl p-6 border border-yellow-200 dark:border-yellow-800">
                <h4 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center">
                  <Award className="mr-2 h-5 w-5 text-yellow-600" />
                  Achievements & Recognition
                </h4>
                <div className="grid md:grid-cols-2 gap-4">
                  {resumeData.achievements.map((achievement, index) => (
                    <div key={index} className="flex items-start space-x-3 bg-white dark:bg-slate-800 p-4 rounded-lg border border-yellow-200 dark:border-yellow-700">
                      <div className="w-8 h-8 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center flex-shrink-0">
                        <Award className="h-4 w-4 text-white" />
                      </div>
                      <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">{achievement}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Certifications */}
            {resumeData?.certifications && resumeData.certifications.length > 0 && (
              <div className="bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/20 dark:to-teal-900/20 rounded-xl p-6 border border-emerald-200 dark:border-emerald-800">
                <h4 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center">
                  <Award className="mr-2 h-5 w-5 text-emerald-600" />
                  Professional Certifications
                </h4>
                <div className="flex flex-wrap gap-3">
                  {resumeData.certifications.map((cert, index) => (
                    <Badge 
                      key={index} 
                      className="px-4 py-2 text-sm font-medium bg-gradient-to-r from-emerald-100 to-teal-100 text-emerald-800 border-emerald-200 hover:from-emerald-200 hover:to-teal-200 transition-all duration-200 dark:from-emerald-900 dark:to-teal-900 dark:text-emerald-200 dark:border-emerald-700"
                    >
                      <Award className="mr-2 h-3 w-3" />
                      {cert}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Courses & Training */}
            {resumeData?.courses_undertaken && resumeData.courses_undertaken.length > 0 && (
              <div className="bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 rounded-xl p-6 border border-blue-200 dark:border-blue-800">
                <h4 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center">
                  <GraduationCap className="mr-2 h-5 w-5 text-blue-600" />
                  Additional Courses & Training
                </h4>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {resumeData.courses_undertaken.map((course, index) => (
                    <div key={index} className="flex items-center space-x-2 bg-white dark:bg-slate-800 p-3 rounded-lg border border-blue-200 dark:border-blue-700 hover:shadow-md transition-shadow duration-200">
                      <div className="w-6 h-6 bg-gradient-to-br from-blue-400 to-cyan-500 rounded-full flex items-center justify-center flex-shrink-0">
                        <GraduationCap className="h-3 w-3 text-white" />
                      </div>
                      <span className="text-sm text-gray-700 dark:text-gray-300 font-medium">{course}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            </div>
          </CardContent>
          {/* Scroll indicator gradient */}
          <div className="absolute bottom-0 left-0 right-0 h-8 bg-gradient-to-t from-white dark:from-slate-800 to-transparent pointer-events-none opacity-70"></div>
        </Card>
      )}

      {/* No Data Message */}
      {!hasJobPreferences && !hasResumeData && (
        <Card className="text-center py-8">
          <CardContent>
            <User className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">Complete Your Profile</h3>
            <p className="text-gray-500 dark:text-gray-400 mb-4">
              Add your job preferences and upload your resume to get personalized job recommendations.
            </p>
            <Button onClick={onEditClick} className="mr-2">
              <Edit className="mr-2 h-4 w-4" />
              Update Profile
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default UserProfile;
