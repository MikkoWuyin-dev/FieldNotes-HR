#!/usr/bin/env bash
# Repeatable HTTP status check for every URL cited in the learning library.
# The generating sandbox had allowlisted egress, so the original sweep could not
# run there (see RETROSPECTIVE.md). It now runs weekly in GitHub Actions
# (.github/workflows/link-check.yml); locally, run: make links
# First CI result (run 40471064309, 2026-10-27): 30 URLs, 27 x 200, 3 x 403.
# A 403 can be bot filtering; a 526 can be an origin TLS issue; 000 means no response.
# Status codes alone never prove that a resource is free - read the provider page
# and record what you find in src/verification-manifest.json.
set -u
printf "status\turl\n"
urls=(
  "https://www.youtube.com/playlist?list=PLeDNHX61_qlQeRK1_i5flRpz2T0wjQXN2"
  "https://www.youtube.com/playlist?list=PLeDNHX61_qlQWYcxZNB19TDOKbl625W2c"
  "https://learn.saylor.org/course/view.php?id=1292"
  "https://openstax.org/books/principles-management/pages/11-introduction"
  "https://www.open.edu/openlearn/money-business/human-resources/human-resources-recruitment-and-selection/content-section-0"
  "https://alison.com/course/diploma-in-human-resources-hr"
  "https://learn.saylor.org/course/BUS301"
  "https://www.coursera.org/learn/recruiting-hiring-onboarding-employees"
  "https://learner.coursera.help/hc/en-us/articles/209818613-Enrollment-options"
  "https://www.onetonline.org/"
  "https://resources.workable.com/hr-templates/"
  "https://support.greenhouse.io/hc/en-us/articles/360007245452-Structured-hiring-Introduction"
  "https://resources.workable.com/boolean-search-cheatsheets/"
  "https://www.youtube.com/watch?v=yMnw_2VNOVE"
  "https://rework.withgoogle.com/intl/en/guides/"
  "https://www.jobberman.com/employer/free-listing"
  "https://www.greenhouse.com/guidance"
  "https://rework.withgoogle.com/intl/en/guides/a-guide-to-structured-interviewing-for-better-hiring-practices"
  "https://rework.withgoogle.com/intl/en/guides/effective-interviewer-training-for-better-candidate-experiences"
  "https://ndpc.gov.ng/wp-content/uploads/2025/07/NDP-ACT-GAID-2025-MARCH-20TH.pdf"
  "https://lawsofnigeria.placng.org/laws/L1.pdf"
  "https://academy.hubspot.com/lessons/managing-your-contacts-with-the-hubspot-crm"
  "https://cipmnigeria.org/membership/membership-routes/"
  "https://www.linkedin.com/learning/"
  "https://www.linkedin.com/help/recruiter/answer/a6807901"
  "https://www.coursera.org/learn/aphri-talent-acquisition-and-onboarding"
  "https://www.aihr.com/courses/sourcing-recruitment-certification/"
  "https://www.udemy.com/course/recruiter-training-hire-top-employees-in-30-days/"
  "https://helpcenter.alison.com/en/articles/8206417-is-alison-really-free"
  "https://support.saylor.org/hc/en-us/articles/23586212781844-FAQ-General"
  "https://learn.saylor.org/mod/page/view.php?id=94644"
  "https://www.jobberman.com/job-seeker"
  # Current Stage 3–8 evidence URLs; the historical sweep record above remains unchanged.
  "https://resources.workable.com/recruiter-job-description"
  "https://resources.workable.com/hire-hr-directors-boolean-search-strings"
  "https://rework.withgoogle.com/intl/en/guides/how-to-create-a-positive-experience-for-candidates"
  "https://www.open.edu/openlearn/money-business/human-resources/human-resources-recruitment-and-selection/content-section-4.10/"
  "https://www.youtube.com/watch?v=zariLo_tX00"
  "https://rework.withgoogle.com/intl/en/guides/a-data-driven-approach-to-optimizing-employee-onboarding"
  "https://www.hubspot.com/products/crm"
  "https://www.greenhouse.com/recruiting-benchmarks"
  "https://cdn.prod.website-files.com/6668a687e71e2722fccb8357/6af3aa54e0a5c01ffec1552e_The-Hire-Standard-Fall-2026_US.pdf"
  "https://www.youtube.com/watch?v=LPzWMrLvMGY"
)
for url in "${urls[@]}"; do
  code=$(curl -sS -o /dev/null -w "%{http_code}" -L --max-time 25 "$url" 2>/dev/null || echo 000)
  printf "%s\t%s\n" "$code" "$url"
done
