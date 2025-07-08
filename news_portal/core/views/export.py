import csv
from django.http import HttpResponse, Http404
from reportlab.pdfgen import canvas
from core.models.article import Article
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


@login_required
def export_article_csv(request, pk):
    """
    Exports a single article to CSV.
    """
    article = get_object_or_404(Article, pk=pk)

    # Limit access to approved articles only for non-author users
    if (
        article.status != "approved"
        and request.user != article.author
        and request.user.role != "editor"
    ):
        raise Http404("You do not have permission to export this article.")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="{article.title[:50]}_article.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(["Title", "Author", "Status", "Approved At"])
    writer.writerow(
        [article.title, article.author.username, article.status, article.approved_at]
    )

    return response


@login_required
def export_article_pdf(request, pk):
    """
    Exports a single article to PDF.
    """
    article = get_object_or_404(Article, pk=pk)

    if (
        article.status != "approved"
        and request.user != article.author
        and request.user.role != "editor"
    ):
        raise Http404("You do not have permission to export this article.")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{article.title[:50]}_article.pdf"'
    )

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 14)
    p.drawString(30, 800, f"Title: {article.title}")
    p.setFont("Helvetica", 12)
    p.drawString(30, 780, f"Author: {article.author.username}")
    p.drawString(30, 760, f"Status: {article.status}")
    p.drawString(
        30, 740, f"Approved At: {article.approved_at if article.approved_at else '—'}"
    )
    p.drawString(30, 720, "Content:")
    p.setFont("Helvetica", 11)

    y = 700
    for line in article.content.splitlines():
        p.drawString(30, y, line.strip())
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response
