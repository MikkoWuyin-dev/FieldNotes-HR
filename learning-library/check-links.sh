#!/usr/bin/env bash
# Repeatable HTTP status check for every URL cited in the learning library.
# NOT RUN in the generating sandbox: outbound traffic there is allowlisted.
# Run this on your own machine:  bash check-links.sh > link-status.tsv
# A 403 can be bot filtering; a 526 can be an origin TLS issue; 000 means no response.
# Status codes alone never prove that a resource is free - read the provider page.
set -u
printf "status\turl\n"
urls=(
  "https://www.youtube.com/@HRLearningLab"
  "https://learn.saylor.org/course/view.php?id=1292"
  "https://openstax.org/books/principles-management/pages/11-introduction"
  "https://www.open.edu/openlearn/money-business/human-resources/human-resources-recruitment-and-selection/content-section-0"
  "https://alison.com/course/diploma-in-human-resources-hr"
  "https://learn.saylor.org/course/BUS301"
  "https://www.coursera.org/learn/recruiting-hiring-onboarding-employees"
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
)
for url in "${urls[@]}"; do
  code=$(curl -sS -o /dev/null -w "%{http_code}" -L --max-time 25 "$url" 2>/dev/null || echo 000)
  printf "%s\t%s\n" "$code" "$url"
done
