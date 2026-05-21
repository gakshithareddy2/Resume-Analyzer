from pathlib import Path
import json

from extractors import extract_text_from_file
from cleaner import clean_text, clean_section_text
from segmenter import segment_resume

from contact_extractor import extract_contact_info
from name_extractor import extract_name
from skill_extractor import extract_skills
from entity_extractor import extract_entities

from matcher import calculate_match_score


class ResumeParser:

    def __init__(self):

        self.base_dir = Path(__file__).resolve().parent.parent

        self.resume_folder = self.base_dir / "data" / "sample_resumes"

        self.text_output_folder = (
            self.base_dir / "output" / "extracted_text"
        )

        self.sections_output_folder = (
            self.base_dir / "output" / "sections"
        )

        self.job_description_file = (
            self.base_dir / "data" / "job_description.txt"
        )

        self.text_output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        self.sections_output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    def fix_score_consistency(self, job_match, sections):

        score_breakdown = job_match.get("score_breakdown", {})

        if not score_breakdown:
            score_breakdown = {
                "skills_score": 0,
                "projects_score": 0,
                "education_gpa_score": 0,
                "experience_score": 0
            }

        if sections.get("projects", "0") == "0":
            score_breakdown["projects_score"] = 0

        if sections.get("education", "0") == "0":
            score_breakdown["education_gpa_score"] = 0

        if sections.get("experience", "0") == "0":
            score_breakdown["experience_score"] = 0

        skills_score = score_breakdown.get("skills_score", 0)
        projects_score = score_breakdown.get("projects_score", 0)
        education_score = score_breakdown.get("education_gpa_score", 0)
        experience_score = score_breakdown.get("experience_score", 0)

        job_match["score_breakdown"] = score_breakdown

        job_match["match_percentage"] = round(
            skills_score
            + projects_score
            + education_score
            + experience_score,
            2
        )

        return job_match

    def parse_file(self, file_path, job_description=None):

        file_path = Path(file_path)

        raw_text = extract_text_from_file(file_path)

        cleaned_text = clean_text(raw_text)

        sections = segment_resume(cleaned_text)

        sections = {
            key: clean_section_text(value)
            for key, value in sections.items()
        }

        candidate_name = extract_name(cleaned_text)

        contact_info = extract_contact_info(cleaned_text)

        detected_skills = extract_skills(cleaned_text)

        entities = extract_entities(cleaned_text)

        if job_description and job_description.strip():

            job_match = calculate_match_score(
                cleaned_text,
                job_description
            )

        elif self.job_description_file.exists():

            with open(
                self.job_description_file,
                "r",
                encoding="utf-8"
            ) as file:

                saved_job_description = file.read()

            job_match = calculate_match_score(
                cleaned_text,
                saved_job_description
            )

        else:

            job_match = {
                "match_percentage": 0,
                "score_breakdown": {
                    "skills_score": 0,
                    "projects_score": 0,
                    "education_gpa_score": 0,
                    "experience_score": 0
                },
                "matched_skills": [],
                "missing_skills": []
            }

        job_match = self.fix_score_consistency(
            job_match,
            sections
        )

        final_output = {

            "candidate_name": candidate_name,

            "contact_info": contact_info,

            "detected_skills": detected_skills,

            "entities": entities,

            "job_match": job_match,

            "sections": sections
        }

        text_file_name = f"{file_path.stem}_cleaned.txt"

        with open(
            self.text_output_folder / text_file_name,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(cleaned_text)

        json_file_name = f"{file_path.stem}_sections.json"

        with open(
            self.sections_output_folder / json_file_name,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(final_output, file, indent=4)

        return final_output, cleaned_text


if __name__ == "__main__":

    parser = ResumeParser()

    for file_path in parser.resume_folder.iterdir():

        if file_path.suffix.lower() not in [".pdf", ".docx"]:
            continue

        print(f"\nProcessing: {file_path.name}")

        parser.parse_file(file_path)

        print(f"Completed: {file_path.name}")

    print("\nAll resumes processed successfully!")