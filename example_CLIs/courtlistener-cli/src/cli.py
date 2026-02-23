"""Main Click CLI entry point for CourtListener"""

import click
from .commands.opinions_commands import opinions
from .commands.clusters_commands import clusters
from .commands.opinions_cited_commands import opinions_cited
from .commands.dockets_commands import dockets
from .commands.docket_entries_commands import docket_entries
from .commands.bankruptcy_information_commands import bankruptcy_information
from .commands.originating_court_information_commands import originating_court_information
from .commands.docket_tags_commands import docket_tags
from .commands.recap_documents_commands import recap_documents
from .commands.recap_commands import recap
from .commands.recap_email_commands import recap_email
from .commands.recap_fetch_commands import recap_fetch
from .commands.recap_query_commands import recap_query
from .commands.courts_commands import courts
from .commands.audio_commands import audio
from .commands.people_commands import people
from .commands.positions_commands import positions
from .commands.educations_commands import educations
from .commands.schools_commands import schools
from .commands.political_affiliations_commands import political_affiliations
from .commands.retention_events_commands import retention_events
from .commands.sources_commands import sources
from .commands.aba_ratings_commands import aba_ratings
from .commands.attorneys_commands import attorneys
from .commands.parties_commands import parties
from .commands.financial_disclosures_commands import financial_disclosures
from .commands.agreements_commands import agreements
from .commands.debts_commands import debts
from .commands.gifts_commands import gifts
from .commands.investments_commands import investments
from .commands.non_investment_incomes_commands import non_investment_incomes
from .commands.spouse_incomes_commands import spouse_incomes
from .commands.reimbursements_commands import reimbursements
from .commands.disclosure_positions_commands import disclosure_positions
from .commands.alerts_commands import alerts
from .commands.docket_alerts_commands import docket_alerts
from .commands.memberships_commands import memberships
from .commands.tag_commands import tag
from .commands.tags_commands import tags
from .commands.search_commands import search
from .commands.prayers_commands import prayers
from .commands.visualization_commands import visualization
from .commands.citation_lookup_commands import citation_lookup
from .commands.increment_event_commands import increment_event
from .commands.fjc_integrated_database_commands import fjc_integrated_database


@click.group()
@click.version_option(version='2.0.0')
def main():
    """CourtListener REST API Python CLI Client

    Access federal and state case law, PACER data, RECAP Archive,
    oral arguments, judge information, and financial disclosures.
    """
    pass


# Register command groups
main.add_command(opinions)
main.add_command(clusters)
main.add_command(opinions_cited)
main.add_command(dockets)
main.add_command(docket_entries)
main.add_command(bankruptcy_information)
main.add_command(originating_court_information)
main.add_command(docket_tags)
main.add_command(recap_documents)
main.add_command(recap)
main.add_command(recap_email)
main.add_command(recap_fetch)
main.add_command(recap_query)
main.add_command(courts)
main.add_command(audio)
main.add_command(people)
main.add_command(positions)
main.add_command(educations)
main.add_command(schools)
main.add_command(political_affiliations)
main.add_command(retention_events)
main.add_command(sources)
main.add_command(aba_ratings)
main.add_command(attorneys)
main.add_command(parties)
main.add_command(financial_disclosures)
main.add_command(agreements)
main.add_command(debts)
main.add_command(gifts)
main.add_command(investments)
main.add_command(non_investment_incomes)
main.add_command(spouse_incomes)
main.add_command(reimbursements)
main.add_command(disclosure_positions)
main.add_command(alerts)
main.add_command(docket_alerts)
main.add_command(memberships)
main.add_command(tag)
main.add_command(tags)
main.add_command(search)
main.add_command(prayers)
main.add_command(visualization)
main.add_command(citation_lookup)
main.add_command(increment_event)
main.add_command(fjc_integrated_database)


if __name__ == '__main__':
    main()
